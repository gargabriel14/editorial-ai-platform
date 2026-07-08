"""Scoring logic for editorial opportunities."""

from __future__ import annotations

from editorial_ai.core.models import MarketSnapshot, Opportunity, TrendSignal
from editorial_ai.core.utils import clamp_score, stable_id, utc_now_iso


def score_opportunity(signal: TrendSignal, market: MarketSnapshot) -> float:
    """Score a book opportunity from 0 to 100.

    Competition is inverted because lower competition is better.
    """
    competitive_fit = 100 - clamp_score(market.competition_score)
    total = (
        clamp_score(signal.demand_score) * 0.30
        + clamp_score(signal.momentum_score) * 0.25
        + clamp_score(market.margin_score) * 0.18
        + clamp_score(market.seo_score) * 0.17
        + competitive_fit * 0.10
    )
    return clamp_score(total)


def build_opportunity(signal: TrendSignal, market: MarketSnapshot) -> Opportunity:
    total = score_opportunity(signal, market)
    rationale = (
        f"Demand {signal.demand_score:.0f}, trend {signal.momentum_score:.0f}, "
        f"competition {market.competition_score:.0f}, margin {market.margin_score:.0f}."
    )
    return Opportunity(
        id=stable_id(signal.niche, market.title_angle, prefix="opp"),
        niche=signal.niche,
        title_angle=market.title_angle,
        audience=market.audience,
        demand_score=clamp_score(signal.demand_score),
        trend_score=clamp_score(signal.momentum_score),
        competition_score=clamp_score(market.competition_score),
        margin_score=clamp_score(market.margin_score),
        seo_score=clamp_score(market.seo_score),
        total_score=total,
        status="discovered",
        source=f"{signal.source}+{market.source}",
        rationale=rationale,
        keywords=signal.keywords,
        created_at=utc_now_iso(),
    )

