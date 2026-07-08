"""Publication readiness service."""

from __future__ import annotations

from editorial_ai.core.models import Opportunity, PublicationPackage, SeoPack


class PublishingService:
    """Build a publication checklist and metadata package."""

    def package(self, opportunity: Opportunity, seo_pack: SeoPack) -> PublicationPackage:
        return PublicationPackage(
            opportunity_id=opportunity.id,
            checklist=(
                "Validate final manuscript originality and citations.",
                "Run editorial QA: structure, claims, spelling and formatting.",
                "Validate current KDP categories before upload.",
                "Prepare cover, A+ assets and sample preview.",
                "Human approval before publication.",
            ),
            metadata={
                "title": seo_pack.title,
                "subtitle": seo_pack.subtitle,
                "primary_audience": opportunity.audience,
                "status": "ready_for_human_review",
            },
            approval_required=True,
        )

