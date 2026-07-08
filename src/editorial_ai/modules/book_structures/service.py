"""Book outline generation."""

from __future__ import annotations

from editorial_ai.core.models import BookStructure, Chapter, Opportunity


class BookStructureService:
    """Create a reusable structure for practical non-fiction books."""

    def build(self, opportunity: Opportunity) -> BookStructure:
        chapters = (
            Chapter(
                number=1,
                title="Mapa del lector y resultado esperado",
                objective="Definir el problema, el lector ideal y la promesa concreta.",
                deliverable="Diagnostico inicial y objetivo de 30 dias.",
            ),
            Chapter(
                number=2,
                title="Principios esenciales",
                objective="Explicar los conceptos minimos para avanzar sin friccion.",
                deliverable="Resumen de principios y errores comunes.",
            ),
            Chapter(
                number=3,
                title="Plan de accion semanal",
                objective="Convertir la teoria en un calendario de tareas realista.",
                deliverable="Plan de cuatro semanas.",
            ),
            Chapter(
                number=4,
                title="Ejercicios y plantillas",
                objective="Dar herramientas repetibles para aplicar el metodo.",
                deliverable="Plantillas listas para copiar.",
            ),
            Chapter(
                number=5,
                title="Medicion y mejora",
                objective="Medir progreso, detectar bloqueos y ajustar el sistema.",
                deliverable="Scorecard de seguimiento.",
            ),
            Chapter(
                number=6,
                title="Siguiente nivel",
                objective="Proponer rutas de continuidad y productos relacionados.",
                deliverable="Checklist final y recomendaciones.",
            ),
        )
        return BookStructure(
            opportunity_id=opportunity.id,
            working_title=opportunity.title_angle,
            reader_promise=f"El lector podra aplicar {opportunity.niche} con un sistema simple.",
            chapters=chapters,
            bonus_assets=(
                "Checklist imprimible",
                "Plantilla de seguimiento semanal",
                "Pagina de recursos actualizable",
            ),
        )

