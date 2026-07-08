"""Amazon/KDP metadata and SEO pack generation."""

from __future__ import annotations

from editorial_ai.core.models import Opportunity, SeoPack


class AmazonSEOService:
    """Generate reusable SEO metadata for KDP publication workflows."""

    def build_pack(self, opportunity: Opportunity) -> SeoPack:
        keywords = self._dedupe(
            [
                *opportunity.keywords,
                "guia practica",
                "libro paso a paso",
                opportunity.audience,
                "ejercicios",
                "plantillas",
            ]
        )
        return SeoPack(
            opportunity_id=opportunity.id,
            title=opportunity.title_angle,
            subtitle=f"Metodo claro para {opportunity.audience} con ejercicios y plantillas",
            backend_keywords=tuple(keywords[:7]),
            description_bullets=(
                f"Transforma {opportunity.niche} en un plan accionable.",
                "Incluye ejercicios breves, checklist y seguimiento semanal.",
                "Pensado para lectura rapida y aplicacion inmediata.",
            ),
            category_candidates=(
                "No ficcion practica",
                "Educacion y referencia",
                "Empresa, carrera o desarrollo personal",
            ),
        )

    @staticmethod
    def _dedupe(values: list[str]) -> list[str]:
        seen: set[str] = set()
        clean: list[str] = []
        for value in values:
            normalized = " ".join(str(value).lower().split())
            if normalized and normalized not in seen:
                seen.add(normalized)
                clean.append(normalized)
        return clean

