"""Analytics service for event recording and summaries."""

from __future__ import annotations

from collections import defaultdict

from editorial_ai.core.models import AnalyticsEvent
from editorial_ai.core.ports import OpportunityRepository
from editorial_ai.core.utils import utc_now_iso


class AnalyticsService:
    """Record business events and produce simple KPI summaries."""

    def __init__(self, repository: OpportunityRepository) -> None:
        self.repository = repository

    def record(self, event_name: str, entity_id: str, value: float, **metadata: str) -> None:
        self.repository.record_event(
            AnalyticsEvent(
                event_name=event_name,
                entity_id=entity_id,
                value=value,
                metadata=metadata,
                created_at=utc_now_iso(),
            )
        )

    def summarize(self, events: list[AnalyticsEvent]) -> dict[str, float]:
        totals: dict[str, float] = defaultdict(float)
        for event in events:
            totals[event.event_name] += event.value
        return dict(totals)

