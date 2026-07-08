"""Opportunity creation and persistence."""

from __future__ import annotations

from typing import Iterable

from editorial_ai.core.models import MarketSnapshot, Opportunity, TrendSignal
from editorial_ai.core.ports import OpportunityRepository
from editorial_ai.core.scoring import build_opportunity
from editorial_ai.core.utils import clamp_score


class OpportunityService:
    """Turn research signals into scored editorial opportunities."""

    def __init__(self, repository: OpportunityRepository) -> None:
        self.repository = repository

    def create_from_signals(self, signals: Iterable[TrendSignal]) -> list[Opportunity]:
        opportunities: list[Opportunity] = []
        for signal in signals:
            market = self._snapshot_from_signal(signal)
            opportunity = build_opportunity(signal, market)
            self.repository.upsert_opportunity(opportunity)
            opportunities.append(opportunity)
        return sorted(opportunities, key=lambda item: item.total_score, reverse=True)

    @staticmethod
    def _snapshot_from_signal(signal: TrendSignal) -> MarketSnapshot:
        niche_len = len(signal.niche)
        keyword_count = len(signal.keywords)
        competition = 38 + (niche_len % 36) - min(keyword_count * 2, 10)
        margin = 62 + min(keyword_count * 4, 18)
        seo = 54 + min(keyword_count * 5, 30)
        title_angle = f"{signal.niche}: guia practica en 30 dias"
        return MarketSnapshot(
            niche=signal.niche,
            title_angle=title_angle,
            audience=signal.audience_hint,
            competition_score=clamp_score(competition),
            margin_score=clamp_score(margin),
            seo_score=clamp_score(seo),
            source="market_snapshot_heuristic_v1",
            notes="Replace with Keepa, Amazon ads, KDP reports or keyword API data.",
        )

