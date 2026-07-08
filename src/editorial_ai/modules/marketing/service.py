"""Marketing plan generation."""

from __future__ import annotations

from editorial_ai.core.models import MarketingPlan, Opportunity


class MarketingService:
    """Build a basic launch plan that can be automated through n8n."""

    def build_plan(self, opportunity: Opportunity) -> MarketingPlan:
        return MarketingPlan(
            opportunity_id=opportunity.id,
            positioning=f"Libro practico para {opportunity.audience}: {opportunity.niche}.",
            launch_tasks=(
                "Create landing page and waitlist.",
                "Generate 10 short-form content angles from book chapters.",
                "Prepare launch email sequence.",
                "Run low-budget Amazon Ads keyword test.",
                "Collect reviews from approved beta readers.",
            ),
            content_calendar=(
                "Day -14: problem education post.",
                "Day -10: checklist lead magnet.",
                "Day -7: behind the scenes of the method.",
                "Day -3: sample chapter or template.",
                "Day 0: launch announcement.",
                "Day +7: case study or reader result.",
            ),
            paid_test_budget_eur=50.0,
        )

