"""Ports that keep business logic independent from external providers."""

from __future__ import annotations

from typing import Protocol, Sequence

from editorial_ai.core.models import AnalyticsEvent, Opportunity, TrendSignal


class TrendSource(Protocol):
    def collect(self, seed_topics: Sequence[str]) -> list[TrendSignal]:
        """Return trend signals from an external or internal source."""


class OpportunityRepository(Protocol):
    def setup(self) -> None:
        """Create required storage structures."""

    def upsert_opportunity(self, opportunity: Opportunity) -> None:
        """Insert or update an opportunity."""

    def list_opportunities(self, limit: int = 25, min_score: float = 0) -> list[Opportunity]:
        """Return opportunities sorted by score descending."""

    def record_event(self, event: AnalyticsEvent) -> None:
        """Persist an analytics event."""


class LLMProvider(Protocol):
    def complete(self, system: str, user: str) -> str:
        """Return generated text from an LLM provider."""


class AutomationPublisher(Protocol):
    def publish(self, event_name: str, payload: dict) -> None:
        """Emit an event to an automation system such as n8n."""

