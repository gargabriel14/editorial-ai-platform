"""KDP Launch & Brand Readiness assessment.

The current implementation is deterministic and source-aware. It encodes a
publishable decision model that can later be enriched with live KDP, keyword,
category, ads and marketplace adapters.
"""

from __future__ import annotations

from editorial_ai.core.models import (
    KDPBookTypeRecommendation,
    KDPBrandReadiness,
    KDPComplianceAssessment,
    KDPLaunchPlan,
    KDPLaunchReadiness,
    KDPOptimizationPlan,
    KDPScoreBreakdown,
    KDPSeriesPotential,
    Opportunity,
    SeoPack,
)
from editorial_ai.core.utils import clamp_score


class KDPLaunchReadinessService:
    """Assess whether an opportunity is ready for a KDP launch strategy."""

    REVIEW_POLICY_WARNING = (
        "Reviews may not be required, pressured, incentivized or exchanged. "
        "Free or discounted copies are allowed only when a review is not required "
        "and the reviewer is not influenced."
    )

    def assess(self, opportunity: Opportunity, seo_pack: SeoPack) -> KDPLaunchReadiness:
        theme = self._theme(opportunity)
        book_type = self._book_type(opportunity, theme)
        brand = self._brand(opportunity, theme)
        series = self._series(opportunity, theme)
        optimization = self._optimization(opportunity, seo_pack, theme)
        launch_plan = self._launch_plan(opportunity, theme)
        compliance = self._compliance(opportunity, theme)
        score = self._score(opportunity, book_type, brand, series, compliance, theme)
        approval_gate_passed, blockers = self._approval_gate(series, compliance, score)
        recommendation = self._recommendation(score, approval_gate_passed, series, compliance)
        return KDPLaunchReadiness(
            opportunity_id=opportunity.id,
            book_type=book_type,
            brand=brand,
            series=series,
            optimization=optimization,
            launch_plan=launch_plan,
            compliance=compliance,
            score=score,
            recommendation=recommendation,
            approval_gate_passed=approval_gate_passed,
            approval_blockers=blockers,
        )

    def _theme(self, opportunity: Opportunity) -> str:
        text = " ".join((opportunity.niche, opportunity.title_angle, *opportunity.keywords)).lower()
        if "freelance" in text or "productividad" in text:
            return "freelance_productivity"
        if "prompt" in text or "profesor" in text or "docente" in text:
            return "teacher_ai"
        if "mindfulness" in text or "adolescente" in text:
            return "teen_mindfulness"
        if "finanza" in text or "creativo" in text:
            return "creative_finance"
        if "cuaderno" in text or "planner" in text or "journal" in text:
            return "low_content"
        return "practical_nonfiction"

    def _book_type(self, opportunity: Opportunity, theme: str) -> KDPBookTypeRecommendation:
        if theme == "low_content":
            return KDPBookTypeRecommendation(
                content_level="Bajo contenido",
                primary_format="paperback",
                secondary_formats=("hardcover",),
                rationale="La promesa se apoya en paginas rellenables y repetibles.",
            )
        if theme in {"teen_mindfulness", "creative_finance"}:
            return KDPBookTypeRecommendation(
                content_level="Mixto",
                primary_format="paperback",
                secondary_formats=("ebook", "hardcover"),
                rationale="Combina explicacion breve, ejercicios guiados y plantillas.",
            )
        return KDPBookTypeRecommendation(
            content_level="Alto contenido",
            primary_format="ebook + paperback",
            secondary_formats=("hardcover",),
            rationale=f"{opportunity.niche} requiere explicacion, metodo y casos practicos.",
        )

    def _brand(self, opportunity: Opportunity, theme: str) -> KDPBrandReadiness:
        presets = {
            "freelance_productivity": (
                "Freelance Focus Studio",
                "Sistemas simples para trabajar mejor sin convertirse en una empresa grande.",
                "Cubiertas limpias, verde profundo, grillas, checklists y tipografia sans.",
                "Directo, practico, adulto y orientado a accion.",
                "Freelancers, consultores y creativos independientes.",
                "Marca paraguas para productividad, finanzas, clientes y rutinas freelance.",
            ),
            "teacher_ai": (
                "Aula IA Practica",
                "IA aplicable en clase con controles pedagogicos y baja friccion.",
                "Azules claros, pizarras, iconografia educativa y mockups de prompts.",
                "Didactico, responsable, claro y actualizado.",
                "Profesores, formadores y coordinadores academicos.",
                "Marca paraguas viable si se actualiza por asignatura, edad y herramienta.",
            ),
            "teen_mindfulness": (
                "Calma Joven",
                "Herramientas emocionales simples para adolescentes y familias.",
                "Paleta clara, ilustracion suave, espacios de escritura y tono calmado.",
                "Empatico, seguro, no clinico y acompanante.",
                "Familias, educadores y adolescentes con apoyo adulto.",
                "Marca paraguas para cuadernos, planners y guias emocionales por edad.",
            ),
            "creative_finance": (
                "Creative Money Lab",
                "Finanzas simples para creativos que no quieren hojas de calculo eternas.",
                "Cubiertas sobrias con acentos vivos, diagramas y plantillas.",
                "Cercano, pragmatico y sin jerga financiera pesada.",
                "Disenadores, escritores, artistas y freelancers creativos.",
                "Marca paraguas para pricing, presupuestos, impuestos y flujo de caja.",
            ),
        }
        imprint, value, visual, tone, audience, umbrella = presets.get(
            theme,
            (
                "Practical Pages Lab",
                "Guias accionables con ejercicios y recursos descargables.",
                "Cubiertas limpias, alto contraste y senales visuales de progreso.",
                "Claro, util y sin relleno.",
                opportunity.audience,
                "Marca paraguas por problemas practicos y soluciones en 30 dias.",
            ),
        )
        return KDPBrandReadiness(
            imprint_name=imprint,
            value_proposition=value,
            visual_identity=visual,
            editorial_tone=tone,
            target_audience=audience,
            umbrella_strategy=umbrella,
        )

    def _series(self, opportunity: Opportunity, theme: str) -> KDPSeriesPotential:
        if theme == "freelance_productivity":
            titles = (
                "Rutinas de foco para freelancers",
                "Gestion de clientes para freelancers",
                "Finanzas simples para freelancers",
                "Sistema semanal para creativos independientes",
                "Plantillas de productividad freelance",
            )
            complements = (
                "workbook",
                "planner semanal",
                "checklist de revision diaria",
                "plantillas Notion/Sheets",
                "lead magnet",
                "curso digital corto",
                "audiolibro",
            )
            rationale = "Evergreen, audiencia homogenea y problemas repetibles por subtema."
            count = 8
        elif theme == "teacher_ai":
            titles = (
                "Prompts de IA para planificar clases",
                "IA para evaluaciones formativas",
                "Prompts por asignatura para secundaria",
                "IA responsable para coordinadores docentes",
                "Plantillas de prompts para profesores ocupados",
            )
            complements = (
                "prompt workbook",
                "plantillas descargables",
                "lead magnet",
                "curso digital",
                "traduccion",
                "checklist de uso responsable",
            )
            rationale = "Serie viable, pero necesita actualizaciones por obsolescencia de herramientas."
            count = 6
        elif theme == "teen_mindfulness":
            titles = (
                "Cuaderno de calma para adolescentes",
                "Mindfulness para examenes",
                "Diario de emociones para familias",
                "Planner de habitos tranquilos",
                "Respiracion y foco para estudiantes",
            )
            complements = ("planner", "audio guiado", "checklist familiar", "lead magnet", "workbook")
            rationale = "Serie viable por edad, contexto escolar y formato guiado."
            count = 7
        else:
            titles = (
                f"{opportunity.niche}: ejercicios avanzados",
                f"{opportunity.niche}: workbook practico",
                f"{opportunity.niche}: planner de seguimiento",
                f"{opportunity.niche}: checklist esencial",
                f"{opportunity.niche}: casos y ejemplos",
            )
            complements = ("workbook", "planner", "checklist", "plantillas", "lead magnet")
            rationale = "Potencial moderado si el primer libro valida audiencia y formato."
            count = 5
        return KDPSeriesPotential(
            can_be_series=count >= 5,
            potential_titles_count=count,
            suggested_next_titles=titles,
            complementary_products=complements,
            rationale=rationale,
        )

    def _optimization(
        self,
        opportunity: Opportunity,
        seo_pack: SeoPack,
        theme: str,
    ) -> KDPOptimizationPlan:
        categories_by_theme = {
            "freelance_productivity": (
                (
                    "Business & Money > Skills > Time Management",
                    "Business & Money > Small Business & Entrepreneurship",
                    "Self-Help > Personal Transformation > Time Management",
                ),
                (
                    "Business & Money > Job Hunting & Careers",
                    "Computers & Technology > Business Technology",
                ),
                "Media",
                "Evitar categorias demasiado amplias de autoayuda sin validar competidores.",
                "productividad freelance",
            ),
            "teacher_ai": (
                (
                    "Education & Teaching > Schools & Teaching",
                    "Education & Teaching > Computers & Technology",
                    "Reference > Education",
                ),
                (
                    "Computers & Technology > Artificial Intelligence",
                    "Education & Teaching > Teacher Resources",
                ),
                "Alta",
                "Alta competencia y obsolescencia; validar categoria exacta antes de publicar.",
                "prompts IA profesores",
            ),
            "teen_mindfulness": (
                (
                    "Teen & Young Adult > Health, Mind & Body",
                    "Self-Help > Stress Management",
                    "Education & Teaching > Studying & Workbooks",
                ),
                (
                    "Parenting & Relationships > Family Activities",
                    "Health, Fitness & Dieting > Mental Health",
                ),
                "Media",
                "Cuidar claims de salud mental; no posicionar como terapia.",
                "mindfulness adolescentes",
            ),
            "creative_finance": (
                (
                    "Business & Money > Personal Finance",
                    "Business & Money > Entrepreneurship",
                    "Arts & Photography > Business of Art",
                ),
                (
                    "Self-Help > Personal Success",
                    "Business & Money > Accounting",
                ),
                "Media",
                "Evitar promesas financieras garantizadas o asesoramiento personalizado.",
                "finanzas creativos",
            ),
        }
        recommended, alternatives, competition, risk, cover_keyword = categories_by_theme.get(
            theme,
            (
                tuple(seo_pack.category_candidates[:3]),
                ("Reference", "Self-Help"),
                "Media",
                "Validar rutas de categoria vigentes en KDP antes de subir.",
                opportunity.keywords[0] if opportunity.keywords else opportunity.niche,
            ),
        )
        return KDPOptimizationPlan(
            seo_title=seo_pack.title,
            seo_subtitle=seo_pack.subtitle,
            backend_keywords=self._seven_keywords(opportunity, seo_pack, theme),
            recommended_categories=recommended,
            alternative_categories=alternatives,
            category_competition_level=competition,
            category_risk=risk,
            cover_primary_keyword=cover_keyword,
        )

    def _seven_keywords(
        self,
        opportunity: Opportunity,
        seo_pack: SeoPack,
        theme: str,
    ) -> tuple[str, ...]:
        theme_keywords = {
            "freelance_productivity": (
                "productividad freelance",
                "habitos para freelancers",
                "organizacion trabajo independiente",
                "sistema semanal freelance",
            ),
            "teacher_ai": (
                "prompts para profesores",
                "ia para docentes",
                "planificar clases con ia",
                "herramientas ia educacion",
            ),
            "teen_mindfulness": (
                "mindfulness adolescentes",
                "cuaderno de calma",
                "diario emocional jovenes",
                "habitos tranquilos estudiantes",
            ),
            "creative_finance": (
                "finanzas para creativos",
                "dinero freelancers creativos",
                "presupuesto artistas",
                "gestion financiera creativa",
            ),
        }
        candidates = [
            *theme_keywords.get(theme, ()),
            *seo_pack.backend_keywords,
            *opportunity.keywords,
            opportunity.audience,
        ]
        clean: list[str] = []
        seen: set[str] = set()
        for value in candidates:
            normalized = " ".join(str(value).lower().split())
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            clean.append(normalized[:50])
            if len(clean) == 7:
                break
        while len(clean) < 7:
            clean.append(f"{opportunity.niche.lower()[:40]} {len(clean) + 1}".strip())
        return tuple(clean)

    def _launch_plan(self, opportunity: Opportunity, theme: str) -> KDPLaunchPlan:
        ads_focus = "keyword exact + phrase"
        if theme == "teacher_ai":
            ads_focus = "keywords long-tail por rol docente y asignatura"
        if theme == "freelance_productivity":
            budget = 75.0
        elif theme == "teacher_ai":
            budget = 60.0
        else:
            budget = 50.0
        return KDPLaunchPlan(
            checklist_30_days=(
                "Validar competidores, BSR aproximado, categorias y promesa de portada.",
                "Definir imprint, serie, lead magnet y pagina de recursos.",
                "Bloquear tabla de contenido y criterios de calidad.",
            ),
            checklist_20_days=(
                "Cerrar borrador completo y assets complementarios.",
                "Preparar portada y A+ Content preliminar.",
                "Crear lista de beta readers sin exigir resena.",
            ),
            checklist_15_days=(
                "QA editorial: claims, originalidad, estructura y ejemplos.",
                "Validar keywords, subtitulo y categorias contra contenido real.",
                "Preparar descripcion KDP y pagina de autor/imprint.",
            ),
            checklist_10_days=(
                "Formatear ebook y paperback.",
                "Revisar prueba impresa o preview digital.",
                "Preparar campana organica y calendario de emails.",
            ),
            checklist_5_days=(
                "Subir borrador final a KDP para revision humana.",
                "Preparar anuncios pausados y tracking de metricas.",
                "Confirmar disclosure AI-generated si aplica.",
            ),
            day_0=(
                "Publicar anuncio organico con promesa especifica.",
                "Activar Amazon Ads con presupuesto controlado.",
                "Registrar baseline de ranking, CTR, CPC y conversion.",
            ),
            days_1_to_5=(
                "Revisar gasto diario y cortar keywords irrelevantes.",
                "Responder aprendizajes en dashboard.",
                "Promover lead magnet y recursos complementarios.",
            ),
            day_14=(
                "Evaluar ventas, conversion, ranking y resenas permitidas.",
                "Ajustar portada, descripcion o keywords si hay baja conversion.",
                "Decidir continuidad de ads.",
            ),
            day_30=(
                "Decidir escala, segundo titulo de serie o backlog.",
                "Documentar aprendizajes en decision log.",
                "Reprocesar score con datos reales.",
            ),
            organic_actions=(
                "Crear 10 piezas cortas desde capitulos y plantillas.",
                "Publicar muestra o checklist como lead magnet.",
                "Contactar comunidades relevantes sin spam ni intercambio de resenas.",
            ),
            amazon_ads_actions=(
                f"Campana Sponsored Products con {ads_focus}.",
                "Separar branded, competitor y generic keywords.",
                "Medir CTR, CPC, conversion, ventas, ranking, resenas y ACOS.",
            ),
            initial_budget_eur=budget,
            metrics_to_track=("CTR", "CPC", "ventas", "ranking", "resenas", "conversion", "ACOS"),
        )

    def _compliance(self, opportunity: Opportunity, theme: str) -> KDPComplianceAssessment:
        if theme == "teacher_ai":
            generic_risk = "Medio-alto: prompts genericos y herramientas cambiantes pueden bajar calidad."
            copyright_risk = "Medio: evitar marcas, capturas o material de herramientas sin derechos."
            risk_level = "Medio-alto"
        elif theme == "teen_mindfulness":
            generic_risk = "Medio: evitar claims terapeuticos y contenido superficial."
            copyright_risk = "Bajo-medio: revisar ilustraciones, ejercicios y claims de salud."
            risk_level = "Medio"
        else:
            generic_risk = "Medio: diferenciar con plantillas, casos y ejemplos propios."
            copyright_risk = "Bajo-medio: revisar marcas citadas, ejemplos y assets visuales."
            risk_level = "Medio-bajo"
        return KDPComplianceAssessment(
            ai_content_disclosure=(
                "Marcar AI-generated si texto, imagenes o traducciones finales fueron creados por IA. "
                "AI-assisted no requiere disclosure, pero debe revisarse manualmente."
            ),
            generic_quality_risk=generic_risk,
            copyright_trademark_risk=copyright_risk,
            review_policy_warning=self.REVIEW_POLICY_WARNING,
            metadata_accuracy_validation=(
                "Titulo, subtitulo, portada, descripcion, categorias y keywords deben representar "
                f"el contenido real de {opportunity.niche}."
            ),
            blocked_review_strategies=(
                "pago por resena",
                "regalo o beneficio condicionado a resena",
                "intercambio de resenas",
                "pedir solo resenas positivas",
                "presionar o influir al lector",
            ),
            risk_level=risk_level,
        )

    def _score(
        self,
        opportunity: Opportunity,
        book_type: KDPBookTypeRecommendation,
        brand: KDPBrandReadiness,
        series: KDPSeriesPotential,
        compliance: KDPComplianceAssessment,
        theme: str,
    ) -> KDPScoreBreakdown:
        demand = opportunity.demand_score
        competition = 100 - opportunity.competition_score
        series_score = 88 if series.can_be_series and series.potential_titles_count >= 6 else 68
        production_ease = {
            "Bajo contenido": 88,
            "Medio contenido": 78,
            "Alto contenido": 66,
            "Mixto": 72,
        }.get(book_type.content_level, 70)
        if theme == "teacher_ai":
            production_ease -= 8
        brand_potential = 86 if "paraguas" in brand.umbrella_strategy.lower() else 72
        if theme == "teacher_ai":
            brand_potential -= 4
        launch_potential = (opportunity.seo_score * 0.55) + (opportunity.margin_score * 0.45)
        automation = 88 if theme in {"freelance_productivity", "teacher_ai"} else 76
        compliance_score = 78
        if compliance.risk_level == "Medio-alto":
            compliance_score = 58
        elif compliance.risk_level == "Medio":
            compliance_score = 68
        total = (
            demand * 0.20
            + competition * 0.15
            + series_score * 0.15
            + production_ease * 0.10
            + brand_potential * 0.15
            + launch_potential * 0.10
            + automation * 0.10
            + compliance_score * 0.05
        )
        total = clamp_score(total)
        explanation = (
            f"Score {total:.1f}: demanda pesa 20%, competencia ajustada {competition:.0f} pesa 15%, "
            f"serie {series_score:.0f} pesa 15%, marca {brand_potential:.0f} pesa 15%. "
            f"La diferencia principal viene de serie/marca, facilidad de produccion y riesgo KDP."
        )
        return KDPScoreBreakdown(
            demand=clamp_score(demand),
            competition=clamp_score(competition),
            series_potential=clamp_score(series_score),
            production_ease=clamp_score(production_ease),
            brand_potential=clamp_score(brand_potential),
            launch_potential=clamp_score(launch_potential),
            automation=clamp_score(automation),
            kdp_compliance=clamp_score(compliance_score),
            total=total,
            explanation=explanation,
        )

    def _approval_gate(
        self,
        series: KDPSeriesPotential,
        compliance: KDPComplianceAssessment,
        score: KDPScoreBreakdown,
    ) -> tuple[bool, tuple[str, ...]]:
        blockers: list[str] = []
        if not series.can_be_series and not series.complementary_products:
            blockers.append("No tiene estrategia de serie ni producto complementario.")
        if compliance.risk_level == "Alto":
            blockers.append("Riesgo KDP/compliance alto sin mitigacion.")
        if compliance.risk_level == "Medio-alto" and score.total < 78:
            blockers.append("Riesgo KDP medio-alto; validar obsolescencia, claims y categorias.")
        if score.total < 70:
            blockers.append("Score KDP inferior a 70; requiere investigacion adicional.")
        return not blockers, tuple(blockers)

    @staticmethod
    def _recommendation(
        score: KDPScoreBreakdown,
        approval_gate_passed: bool,
        series: KDPSeriesPotential,
        compliance: KDPComplianceAssessment,
    ) -> str:
        if compliance.risk_level == "Alto":
            return "Descartar"
        if not approval_gate_passed:
            return "Investigar mas"
        if score.total >= 78 and series.can_be_series:
            return "Convertir en serie"
        if score.total >= 73:
            return "Aprobar piloto"
        if series.complementary_products and score.total >= 68:
            return "Convertir en producto complementario"
        return "Mantener en backlog"
