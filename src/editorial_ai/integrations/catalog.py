"""Catalog of useful APIs and ownership boundaries."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class APIIntegration:
    name: str
    purpose: str
    owner_module: str
    env_vars: tuple[str, ...]
    automation_candidate: str


DEFAULT_API_INTEGRATIONS: tuple[APIIntegration, ...] = (
    APIIntegration(
        name="OpenAI or compatible LLM",
        purpose="Generate outlines, summaries, positioning and QA checklists.",
        owner_module="book_structures, marketing, publishing",
        env_vars=("LLM_API_KEY", "LLM_MODEL"),
        automation_candidate="Generate draft assets after an opportunity passes score threshold.",
    ),
    APIIntegration(
        name="Google Trends / DataForSEO",
        purpose="Collect demand, keyword volume and SERP signals.",
        owner_module="niche_research, trend_analysis",
        env_vars=("TRENDS_API_KEY",),
        automation_candidate="Refresh trend signals daily and notify when momentum changes.",
    ),
    APIIntegration(
        name="Keepa or Amazon marketplace data provider",
        purpose="Estimate Amazon demand, competition and pricing.",
        owner_module="opportunities, seo_amazon",
        env_vars=("MARKETPLACE_API_KEY",),
        automation_candidate="Re-score opportunities before investing in manuscript production.",
    ),
    APIIntegration(
        name="Amazon KDP reports export",
        purpose="Import sales, royalties and ad performance into analytics.",
        owner_module="analytics, publishing",
        env_vars=("KDP_REPORTS_PATH",),
        automation_candidate="Ingest reports weekly and update title-level KPI dashboards.",
    ),
    APIIntegration(
        name="n8n",
        purpose="Connect workflows, approvals, notifications and scheduled runs.",
        owner_module="automations",
        env_vars=("N8N_WEBHOOK_URL",),
        automation_candidate="Trigger the full opportunity pipeline on a schedule.",
    ),
)

