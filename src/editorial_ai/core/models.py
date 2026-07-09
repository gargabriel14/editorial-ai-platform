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
class KDPBookTypeRecommendation:
    content_level: str
    primary_format: str
    secondary_formats: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class KDPBrandReadiness:
    imprint_name: str
    value_proposition: str
    visual_identity: str
    editorial_tone: str
    target_audience: str
    umbrella_strategy: str


@dataclass(frozen=True)
class KDPSeriesPotential:
    can_be_series: bool
    potential_titles_count: int
    suggested_next_titles: tuple[str, ...]
    complementary_products: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class KDPOptimizationPlan:
    seo_title: str
    seo_subtitle: str
    backend_keywords: tuple[str, ...]
    recommended_categories: tuple[str, ...]
    alternative_categories: tuple[str, ...]
    category_competition_level: str
    category_risk: str
    cover_primary_keyword: str


@dataclass(frozen=True)
class KDPLaunchPlan:
    checklist_30_days: tuple[str, ...]
    checklist_20_days: tuple[str, ...]
    checklist_15_days: tuple[str, ...]
    checklist_10_days: tuple[str, ...]
    checklist_5_days: tuple[str, ...]
    day_0: tuple[str, ...]
    days_1_to_5: tuple[str, ...]
    day_14: tuple[str, ...]
    day_30: tuple[str, ...]
    organic_actions: tuple[str, ...]
    amazon_ads_actions: tuple[str, ...]
    initial_budget_eur: float
    metrics_to_track: tuple[str, ...]


@dataclass(frozen=True)
class KDPComplianceAssessment:
    ai_content_disclosure: str
    generic_quality_risk: str
    copyright_trademark_risk: str
    review_policy_warning: str
    metadata_accuracy_validation: str
    blocked_review_strategies: tuple[str, ...]
    risk_level: str


@dataclass(frozen=True)
class KDPScoreBreakdown:
    demand: float
    competition: float
    series_potential: float
    production_ease: float
    brand_potential: float
    launch_potential: float
    automation: float
    kdp_compliance: float
    total: float
    explanation: str


@dataclass(frozen=True)
class KDPLaunchReadiness:
    opportunity_id: str
    book_type: KDPBookTypeRecommendation
    brand: KDPBrandReadiness
    series: KDPSeriesPotential
    optimization: KDPOptimizationPlan
    launch_plan: KDPLaunchPlan
    compliance: KDPComplianceAssessment
    score: KDPScoreBreakdown
    recommendation: str
    approval_gate_passed: bool
    approval_blockers: tuple[str, ...]


@dataclass(frozen=True)
class MarketIntelSignal:
    niche: str
    subniche: str
    time_window: str
    estimated_views: int
    estimated_purchases: int
    search_volume_score: float
    purchase_intent_score: float
    momentum_score: float
    competition_score: float
    kdp_fit_score: float
    total_score: float
    confidence: str
    data_sources: tuple[str, ...]
    rationale: str
    recommended_action: str


@dataclass(frozen=True)
class MarketIntelSnapshot:
    generated_at: str
    provider: str
    windows: tuple[str, ...]
    top_signals: tuple[MarketIntelSignal, ...]
    notes: tuple[str, ...]


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
