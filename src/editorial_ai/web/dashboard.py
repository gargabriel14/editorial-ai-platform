"""Dashboard data builder shared by the web server and tests."""

from __future__ import annotations

from pathlib import Path
from statistics import mean
from typing import Sequence

from editorial_ai.core.defaults import DEFAULT_SEED_TOPICS
from editorial_ai.core.platform import build_default_platform
from editorial_ai.core.storage import SQLiteOpportunityRepository
from editorial_ai.core.utils import to_jsonable, utc_now_iso
from editorial_ai.integrations.catalog import DEFAULT_API_INTEGRATIONS
from editorial_ai.modules.book_structures.service import BookStructureService
from editorial_ai.modules.kdp_launch.service import KDPLaunchReadinessService
from editorial_ai.modules.marketing.service import MarketingService
from editorial_ai.modules.publishing.service import PublishingService
from editorial_ai.modules.seo_amazon.service import AmazonSEOService


def build_dashboard_data(db_path: str | Path, limit: int = 25, min_score: float = 0) -> dict:
    repository = SQLiteOpportunityRepository(db_path)
    repository.setup()
    opportunities = repository.list_opportunities(limit=limit, min_score=min_score)

    structure_service = BookStructureService()
    seo_service = AmazonSEOService()
    publishing_service = PublishingService()
    marketing_service = MarketingService()
    kdp_service = KDPLaunchReadinessService()

    rows = []
    for opportunity in opportunities:
        structure = structure_service.build(opportunity)
        seo_pack = seo_service.build_pack(opportunity)
        publication = publishing_service.package(opportunity, seo_pack)
        marketing = marketing_service.build_plan(opportunity)
        kdp_readiness = kdp_service.assess(opportunity, seo_pack)
        rows.append(
            {
                "opportunity": to_jsonable(opportunity),
                "structure": to_jsonable(structure),
                "seo_pack": to_jsonable(seo_pack),
                "publication": to_jsonable(publication),
                "marketing_plan": to_jsonable(marketing),
                "kdp_launch_readiness": to_jsonable(kdp_readiness),
            }
        )

    scores = [item.total_score for item in opportunities]
    kdp_scores = [row["kdp_launch_readiness"]["score"]["total"] for row in rows]
    recommendations = _count_recommendations(rows)
    kpis = {
        "opportunities": len(opportunities),
        "top_score": max(scores) if scores else 0,
        "average_score": round(mean(scores), 2) if scores else 0,
        "ready_for_review": len([score for score in scores if score >= 70]),
        "top_kdp_score": max(kdp_scores) if kdp_scores else 0,
        "kdp_ready_for_pilot": len(
            [
                row
                for row in rows
                if row["kdp_launch_readiness"]["recommendation"]
                in {"Aprobar piloto", "Convertir en serie"}
            ]
        ),
        "kdp_recommendations": recommendations,
    }
    return {
        "generated_at": utc_now_iso(),
        "kpis": kpis,
        "items": rows,
        "integrations": to_jsonable(DEFAULT_API_INTEGRATIONS),
        "ceo_cto_protocol": build_ceo_cto_protocol(),
    }


def _count_recommendations(rows: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        recommendation = row["kdp_launch_readiness"]["recommendation"]
        counts[recommendation] = counts.get(recommendation, 0) + 1
    return counts


def run_demo_and_build_dashboard(
    db_path: str | Path,
    output_dir: str | Path,
    seed_topics: Sequence[str] | None = None,
) -> dict:
    platform = build_default_platform(db_path)
    result = platform.run_opportunity_pipeline(seed_topics or DEFAULT_SEED_TOPICS)
    platform.export_result(result, output_dir)
    return build_dashboard_data(db_path)


def build_ceo_cto_protocol() -> dict:
    return {
        "source_of_truth": "GitHub repo + docs/decision_log.md + web dashboard",
        "cadence": (
            "Daily: dashboard snapshot. Weekly: CEO decision review. "
            "Monthly: scoring and portfolio strategy update."
        ),
        "channels": [
            {
                "name": "GitHub Issues",
                "use": "Requests, strategic questions and approval gates.",
            },
            {
                "name": "Pull Requests",
                "use": "Implementation review, tests and technical decisions.",
            },
            {
                "name": "n8n",
                "use": "Scheduled syncs, alerts and handoffs between CEO and CTO.",
            },
            {
                "name": "Codex thread",
                "use": "Execution workspace for architecture, code and verification.",
            },
        ],
        "decision_packet": [
            "Context",
            "Options",
            "Recommendation",
            "Risks",
            "Decision owner",
            "Deadline",
        ],
    }
