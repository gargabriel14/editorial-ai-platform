"""Optional FastAPI app for automations and dashboards."""

from __future__ import annotations

import os

from editorial_ai.core.platform import build_default_platform
from editorial_ai.core.storage import SQLiteOpportunityRepository
from editorial_ai.core.utils import to_jsonable
from editorial_ai.integrations.catalog import DEFAULT_API_INTEGRATIONS

try:
    from fastapi import FastAPI
    from pydantic import BaseModel, Field
except ImportError:  # pragma: no cover - optional dependency path
    FastAPI = None  # type: ignore[assignment]
    BaseModel = object  # type: ignore[assignment,misc]
    Field = None  # type: ignore[assignment]


if Field is not None:

    class RunPipelineRequest(BaseModel):
        seed_topics: list[str] = Field(min_length=1)

else:

    class RunPipelineRequest:  # pragma: no cover
        seed_topics: list[str]


def create_app():
    if FastAPI is None:
        raise RuntimeError("Install the api extra: pip install -e '.[api]'")

    app = FastAPI(
        title="Editorial AI Platform",
        version="0.1.0",
        description="Modular operating platform for an AI-first digital publisher.",
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.get("/integrations")
    def integrations() -> dict[str, list[dict]]:
        return {"integrations": to_jsonable(DEFAULT_API_INTEGRATIONS)}

    @app.post("/pipelines/opportunities/run")
    def run_opportunity_pipeline(request: RunPipelineRequest) -> dict:
        db_path = os.getenv("EDITORIAL_DB_PATH", "data/editorial_ai.sqlite")
        platform = build_default_platform(db_path)
        result = platform.run_opportunity_pipeline(request.seed_topics)
        return to_jsonable(result)

    @app.get("/opportunities")
    def list_opportunities(limit: int = 25, min_score: float = 0) -> dict:
        db_path = os.getenv("EDITORIAL_DB_PATH", "data/editorial_ai.sqlite")
        repository = SQLiteOpportunityRepository(db_path)
        repository.setup()
        return {"opportunities": to_jsonable(repository.list_opportunities(limit, min_score))}

    return app


app = create_app() if FastAPI is not None else None

