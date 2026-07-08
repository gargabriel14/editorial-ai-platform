"""Niche discovery service.

This MVP uses deterministic seed analysis. External providers such as
Google Trends, DataForSEO, Exploding Topics or marketplace APIs should be
implemented as TrendSource adapters without changing this service contract.
"""

from __future__ import annotations

import re
from typing import Sequence

from editorial_ai.core.models import TrendSignal
from editorial_ai.core.utils import clamp_score


class NicheResearchService:
    """Create initial niche signals from seed topics."""

    def discover(self, seed_topics: Sequence[str]) -> list[TrendSignal]:
        signals: list[TrendSignal] = []
        for topic in seed_topics:
            cleaned = topic.strip()
            if not cleaned:
                continue
            keywords = tuple(self._keywords(cleaned))
            demand = 58 + (len(cleaned) % 27)
            momentum = 52 + (sum(ord(char) for char in cleaned) % 31)
            signals.append(
                TrendSignal(
                    niche=cleaned,
                    source="seed_research_v1",
                    demand_score=clamp_score(demand),
                    momentum_score=clamp_score(momentum),
                    audience_hint=self._infer_audience(cleaned),
                    keywords=keywords,
                    notes="Seed-derived signal. Replace or enrich with live trend adapters.",
                )
            )
        return signals

    @staticmethod
    def _keywords(topic: str) -> list[str]:
        stopwords = {
            "de",
            "del",
            "para",
            "con",
            "por",
            "los",
            "las",
            "una",
            "unos",
            "unas",
            "the",
            "and",
            "for",
        }
        words = re.findall(r"[A-Za-z0-9]+", topic.lower())
        return [word for word in words if len(word) > 2 and word not in stopwords][:8]

    @staticmethod
    def _infer_audience(topic: str) -> str:
        normalized = topic.lower()
        if "profesor" in normalized or "docente" in normalized:
            return "profesores y formadores"
        if "freelance" in normalized or "emprendedor" in normalized:
            return "profesionales independientes"
        if "adolescente" in normalized or "familia" in normalized:
            return "familias y educadores"
        if "empresa" in normalized or "negocio" in normalized:
            return "pequenas empresas"
        return "lectores de no ficcion practica"

