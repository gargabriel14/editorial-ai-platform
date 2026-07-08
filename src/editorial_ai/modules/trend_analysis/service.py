"""Trend enrichment service."""

from __future__ import annotations

from typing import Iterable

from editorial_ai.core.models import TrendSignal
from editorial_ai.core.utils import clamp_score


class TrendAnalysisService:
    """Normalize and enrich trend signals before opportunity scoring."""

    def enrich(self, signals: Iterable[TrendSignal]) -> list[TrendSignal]:
        enriched: list[TrendSignal] = []
        for signal in signals:
            boost = self._theme_boost(signal)
            enriched.append(
                TrendSignal(
                    niche=signal.niche,
                    source=f"{signal.source}+trend_enrichment_v1",
                    demand_score=clamp_score(signal.demand_score + boost / 2),
                    momentum_score=clamp_score(signal.momentum_score + boost),
                    audience_hint=signal.audience_hint,
                    keywords=signal.keywords,
                    evidence_url=signal.evidence_url,
                    notes=f"{signal.notes} Momentum boost {boost:.0f}.",
                )
            )
        return enriched

    @staticmethod
    def _theme_boost(signal: TrendSignal) -> float:
        text = " ".join((signal.niche, *signal.keywords)).lower()
        boost = 0.0
        if "ia" in text or "ai" in text or "prompt" in text:
            boost += 9
        if "habit" in text or "productividad" in text:
            boost += 5
        if "mindfulness" in text or "ansiedad" in text:
            boost += 4
        if "profesor" in text or "docente" in text:
            boost += 4
        return boost

