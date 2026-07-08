"""Shared domain models for the editorial business."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrendSignal:
    niche: str
    source: str
    demand_score: float
    momentum_score: float
    audience_hint: str
    keywords: tuple[str, ...] = field(default_factory=tuple)
    evidence_url: str | None = None
    notes: str = ""


@dataclass(frozen=True)
class MarketSnapshot:
    niche: str
    title_angle: str
    audience: str
    competition_score: float
    margin_score: float
    seo_score: float
    source: str
    notes: str = ""


@dataclass(frozen=True)
class Opportunity:
    id: str
    niche: str
    title_angle: str
    audience: str
    demand_score: float
    trend_score: float
    competition_score: float
    margin_score: float
    seo_score: float
    total_score: float
    status: str
    source: str
    rationale: str
    keywords: tuple[str, ...]
    created_at: str


@dataclass(frozen=True)
class Chapter:
    number: int
    title: str
    objective: str
    deliverable: str


@dataclass(frozen=True)
class BookStructure:
    opportunity_id: str
    working_title: str
    reader_promise: str
    chapters: tuple[Chapter, ...]
    bonus_assets: tuple[str, ...]


@dataclass(frozen=True)
class SeoPack:
    opportunity_id: str
    title: str
    subtitle: str
    backend_keywords: tuple[str, ...]
    description_bullets: tuple[str, ...]
    category_candidates: tuple[str, ...]


@dataclass(frozen=True)
class PublicationPackage:
    opportunity_id: str
    checklist: tuple[str, ...]
    metadata: dict[str, str]
    approval_required: bool = True


@dataclass(frozen=True)
class MarketingPlan:
    opportunity_id: str
    positioning: str
    launch_tasks: tuple[str, ...]
    content_calendar: tuple[str, ...]
    paid_test_budget_eur: float


@dataclass(frozen=True)
class AnalyticsEvent:
    event_name: str
    entity_id: str
    value: float
    metadata: dict[str, str]
    created_at: str


@dataclass(frozen=True)
class PipelineResult:
    opportunities: tuple[Opportunity, ...]
    structures: tuple[BookStructure, ...]
    seo_packs: tuple[SeoPack, ...]
    marketing_plans: tuple[MarketingPlan, ...]

