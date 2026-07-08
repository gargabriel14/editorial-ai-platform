"""Application orchestration for the modular editorial platform."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from editorial_ai.core.models import PipelineResult
from editorial_ai.core.storage import SQLiteOpportunityRepository
from editorial_ai.core.utils import ensure_parent, to_jsonable
from editorial_ai.modules.book_structures.service import BookStructureService
from editorial_ai.modules.marketing.service import MarketingService
from editorial_ai.modules.niche_research.service import NicheResearchService
from editorial_ai.modules.opportunities.service import OpportunityService
from editorial_ai.modules.seo_amazon.service import AmazonSEOService
from editorial_ai.modules.trend_analysis.service import TrendAnalysisService


class EditorialAIPlatform:
    """Thin orchestrator that wires independent services into workflows."""

    def __init__(
        self,
        niche_research: NicheResearchService,
        trend_analysis: TrendAnalysisService,
        opportunity_service: OpportunityService,
        structure_service: BookStructureService,
        seo_service: AmazonSEOService,
        marketing_service: MarketingService,
    ) -> None:
        self.niche_research = niche_research
        self.trend_analysis = trend_analysis
        self.opportunity_service = opportunity_service
        self.structure_service = structure_service
        self.seo_service = seo_service
        self.marketing_service = marketing_service

    def run_opportunity_pipeline(self, seed_topics: Sequence[str]) -> PipelineResult:
        signals = self.niche_research.discover(seed_topics)
        enriched_signals = self.trend_analysis.enrich(signals)
        opportunities = tuple(self.opportunity_service.create_from_signals(enriched_signals))
        structures = tuple(self.structure_service.build(opportunity) for opportunity in opportunities)
        seo_packs = tuple(self.seo_service.build_pack(opportunity) for opportunity in opportunities)
        marketing_plans = tuple(self.marketing_service.build_plan(opportunity) for opportunity in opportunities)
        return PipelineResult(
            opportunities=opportunities,
            structures=structures,
            seo_packs=seo_packs,
            marketing_plans=marketing_plans,
        )

    def export_result(self, result: PipelineResult, output_dir: str | Path) -> Path:
        target_dir = Path(output_dir)
        target_dir.mkdir(parents=True, exist_ok=True)
        target = ensure_parent(target_dir / "pipeline_result.json")
        target.write_text(json.dumps(to_jsonable(result), indent=2, ensure_ascii=True), encoding="utf-8")
        return target


def build_default_platform(db_path: str | Path = "data/editorial_ai.sqlite") -> EditorialAIPlatform:
    repository = SQLiteOpportunityRepository(db_path)
    repository.setup()
    return EditorialAIPlatform(
        niche_research=NicheResearchService(),
        trend_analysis=TrendAnalysisService(),
        opportunity_service=OpportunityService(repository),
        structure_service=BookStructureService(),
        seo_service=AmazonSEOService(),
        marketing_service=MarketingService(),
    )

