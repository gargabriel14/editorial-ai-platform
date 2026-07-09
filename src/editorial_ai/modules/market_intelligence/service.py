"""KDP market intelligence and niche ranking.

Amazon does not expose global KDP views or purchases by niche through a public
KDP API. This service therefore uses a provider interface and stores explicit
proxy estimates. The default provider is a deterministic seed dataset so the
product workflow works now; production providers should connect Keepa, PA-API,
DataForSEO, Amazon Ads and own KDP reports.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from editorial_ai.core.models import MarketIntelSignal, MarketIntelSnapshot
from editorial_ai.core.storage import SQLiteOpportunityRepository
from editorial_ai.core.utils import clamp_score, utc_now_iso


MARKET_WINDOWS: tuple[str, ...] = ("1y", "6m", "1m", "15d")


@dataclass(frozen=True)
class SeedMarketNiche:
    niche: str
    subniche: str
    base_views: int
    base_purchases: int
    search_volume_score: float
    purchase_intent_score: float
    momentum_score: float
    competition_score: float
    kdp_fit_score: float
    action: str


class MarketIntelProvider(Protocol):
    name: str

    def collect(self) -> list[SeedMarketNiche]:
        """Collect raw market rows from a provider."""


class LocalSeedMarketIntelProvider:
    """Deterministic market proxy until paid/owned data providers are configured."""

    name = "local_kdp_market_proxy_v1"

    def collect(self) -> list[SeedMarketNiche]:
        return [
            SeedMarketNiche(
                "Productividad y carrera",
                "Productividad para freelancers",
                92000,
                4100,
                82,
                78,
                74,
                52,
                88,
                "Aprobar piloto evergreen",
            ),
            SeedMarketNiche(
                "IA practica",
                "Prompts de IA para profesores",
                118000,
                3600,
                90,
                72,
                86,
                68,
                76,
                "Investigar mas por obsolescencia",
            ),
            SeedMarketNiche(
                "Finanzas personales",
                "Presupuesto para creativos",
                76000,
                3300,
                76,
                80,
                66,
                54,
                84,
                "Aprobar investigacion comercial",
            ),
            SeedMarketNiche(
                "Bienestar joven",
                "Mindfulness para adolescentes",
                81000,
                3000,
                79,
                70,
                72,
                57,
                80,
                "Validar claims y formato workbook",
            ),
            SeedMarketNiche(
                "Workbooks educativos",
                "Lectoescritura primaria",
                104000,
                5200,
                88,
                84,
                69,
                72,
                82,
                "Investigar competencia por edad",
            ),
            SeedMarketNiche(
                "Low content",
                "Planners de habitos",
                97000,
                4600,
                84,
                76,
                62,
                79,
                74,
                "Solo si hay diferenciacion de marca",
            ),
            SeedMarketNiche(
                "Idiomas",
                "Ingles para hispanohablantes adultos",
                89000,
                3900,
                83,
                79,
                65,
                64,
                81,
                "Validar serie por nivel",
            ),
            SeedMarketNiche(
                "Cocina saludable",
                "Meal prep economico",
                84000,
                3500,
                81,
                74,
                67,
                61,
                78,
                "Investigar diferenciacion visual",
            ),
            SeedMarketNiche(
                "Espiritualidad practica",
                "Journals de gratitud guiados",
                70000,
                3100,
                73,
                71,
                58,
                70,
                72,
                "Mantener en backlog",
            ),
            SeedMarketNiche(
                "Negocios pequenos",
                "Plantillas para solopreneurs",
                74000,
                3400,
                77,
                78,
                71,
                55,
                86,
                "Aprobar investigacion de producto complementario",
            ),
            SeedMarketNiche(
                "Salud y fitness",
                "Entrenamiento en casa para principiantes",
                99000,
                4300,
                86,
                75,
                64,
                74,
                72,
                "Investigar claims y competencia",
            ),
            SeedMarketNiche(
                "Familia",
                "Rutinas para padres ocupados",
                66000,
                2800,
                70,
                72,
                61,
                49,
                82,
                "Backlog con potencial de serie",
            ),
        ]


class MarketIntelligenceService:
    """Refresh and rank KDP niches across multiple time windows."""

    def __init__(
        self,
        repository: SQLiteOpportunityRepository,
        provider: MarketIntelProvider | None = None,
    ) -> None:
        self.repository = repository
        self.provider = provider or LocalSeedMarketIntelProvider()

    def refresh(self) -> MarketIntelSnapshot:
        rows = self.provider.collect()
        signals: list[MarketIntelSignal] = []
        for window in MARKET_WINDOWS:
            for row in rows:
                signals.append(self._score_row(row, window))
        ranked = sorted(signals, key=lambda signal: signal.total_score, reverse=True)
        snapshot = MarketIntelSnapshot(
            generated_at=utc_now_iso(),
            provider=self.provider.name,
            windows=MARKET_WINDOWS,
            top_signals=tuple(ranked),
            notes=(
                "KDP does not provide public global views or purchases by niche.",
                "Current figures are proxy estimates. Connect Keepa/DataForSEO/Amazon Ads/KDP reports for production data.",
                "Use rankings to prioritize research, not as guaranteed sales claims.",
            ),
        )
        self.repository.save_market_intelligence_snapshot(snapshot)
        return snapshot

    def latest_or_refresh(self) -> MarketIntelSnapshot:
        snapshot = self.repository.latest_market_intelligence_snapshot()
        if snapshot is not None:
            return snapshot
        return self.refresh()

    def top_by_window(self, snapshot: MarketIntelSnapshot, limit: int = 10) -> dict[str, list[dict]]:
        grouped: dict[str, list[MarketIntelSignal]] = {window: [] for window in snapshot.windows}
        for signal in snapshot.top_signals:
            grouped.setdefault(signal.time_window, []).append(signal)
        return {
            window: [
                {
                    "rank": index + 1,
                    "niche": signal.niche,
                    "subniche": signal.subniche,
                    "time_window": signal.time_window,
                    "estimated_views": signal.estimated_views,
                    "estimated_purchases": signal.estimated_purchases,
                    "search_volume_score": signal.search_volume_score,
                    "purchase_intent_score": signal.purchase_intent_score,
                    "momentum_score": signal.momentum_score,
                    "competition_score": signal.competition_score,
                    "kdp_fit_score": signal.kdp_fit_score,
                    "total_score": signal.total_score,
                    "confidence": signal.confidence,
                    "data_sources": list(signal.data_sources),
                    "rationale": signal.rationale,
                    "recommended_action": signal.recommended_action,
                }
                for index, signal in enumerate(grouped.get(window, [])[:limit])
            ]
            for window in snapshot.windows
        }

    def _score_row(self, row: SeedMarketNiche, window: str) -> MarketIntelSignal:
        multiplier = {
            "1y": 1.0,
            "6m": 0.54,
            "1m": 0.11,
            "15d": 0.058,
        }[window]
        momentum_adjustment = {
            "1y": 0,
            "6m": row.momentum_score * 0.03,
            "1m": row.momentum_score * 0.07,
            "15d": row.momentum_score * 0.09,
        }[window]
        estimated_views = int(row.base_views * multiplier * (1 + momentum_adjustment / 100))
        estimated_purchases = int(row.base_purchases * multiplier * (1 + momentum_adjustment / 100))
        competition_fit = 100 - row.competition_score
        total = (
            row.search_volume_score * 0.24
            + row.purchase_intent_score * 0.24
            + row.momentum_score * 0.18
            + competition_fit * 0.14
            + row.kdp_fit_score * 0.20
        )
        total = clamp_score(total + momentum_adjustment)
        rationale = (
            f"{row.subniche} ranks with search {row.search_volume_score:.0f}, "
            f"purchase intent {row.purchase_intent_score:.0f}, momentum {row.momentum_score:.0f}, "
            f"competition {row.competition_score:.0f}."
        )
        return MarketIntelSignal(
            niche=row.niche,
            subniche=row.subniche,
            time_window=window,
            estimated_views=estimated_views,
            estimated_purchases=estimated_purchases,
            search_volume_score=clamp_score(row.search_volume_score),
            purchase_intent_score=clamp_score(row.purchase_intent_score),
            momentum_score=clamp_score(row.momentum_score),
            competition_score=clamp_score(row.competition_score),
            kdp_fit_score=clamp_score(row.kdp_fit_score),
            total_score=total,
            confidence="proxy",
            data_sources=(
                "Amazon BSR proxy",
                "Amazon keyword volume proxy",
                "KDP fit heuristic",
            ),
            rationale=rationale,
            recommended_action=row.action,
        )

