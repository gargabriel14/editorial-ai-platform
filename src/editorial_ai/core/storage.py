"""SQLite storage adapters for the opportunity database and analytics."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path

from editorial_ai.core.models import AnalyticsEvent, Opportunity
from editorial_ai.core.utils import ensure_parent, to_jsonable


class SQLiteOpportunityRepository:
    """Small durable repository suitable for local MVP and n8n automation."""

    def __init__(self, db_path: str | Path) -> None:
        self.db_path = ensure_parent(db_path)

    def setup(self) -> None:
        with closing(self._connect()) as conn:
            with conn:
                conn.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS opportunities (
                        id TEXT PRIMARY KEY,
                        niche TEXT NOT NULL,
                        title_angle TEXT NOT NULL,
                        audience TEXT NOT NULL,
                        total_score REAL NOT NULL,
                        status TEXT NOT NULL,
                        source TEXT NOT NULL,
                        keywords_json TEXT NOT NULL,
                        payload_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );

                    CREATE INDEX IF NOT EXISTS idx_opportunities_score
                    ON opportunities(total_score DESC);

                    CREATE TABLE IF NOT EXISTS analytics_events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event_name TEXT NOT NULL,
                        entity_id TEXT NOT NULL,
                        value REAL NOT NULL,
                        metadata_json TEXT NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    """
                )

    def upsert_opportunity(self, opportunity: Opportunity) -> None:
        payload = json.dumps(to_jsonable(opportunity), ensure_ascii=True)
        keywords = json.dumps(list(opportunity.keywords), ensure_ascii=True)
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO opportunities (
                        id, niche, title_angle, audience, total_score, status,
                        source, keywords_json, payload_json, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        niche=excluded.niche,
                        title_angle=excluded.title_angle,
                        audience=excluded.audience,
                        total_score=excluded.total_score,
                        status=excluded.status,
                        source=excluded.source,
                        keywords_json=excluded.keywords_json,
                        payload_json=excluded.payload_json,
                        created_at=excluded.created_at
                    """,
                    (
                        opportunity.id,
                        opportunity.niche,
                        opportunity.title_angle,
                        opportunity.audience,
                        opportunity.total_score,
                        opportunity.status,
                        opportunity.source,
                        keywords,
                        payload,
                        opportunity.created_at,
                    ),
                )

    def list_opportunities(self, limit: int = 25, min_score: float = 0) -> list[Opportunity]:
        with closing(self._connect()) as conn:
            rows = conn.execute(
                """
                SELECT payload_json
                FROM opportunities
                WHERE total_score >= ?
                ORDER BY total_score DESC, created_at DESC
                LIMIT ?
                """,
                (min_score, limit),
            ).fetchall()
        return [self._row_to_opportunity(row["payload_json"]) for row in rows]

    def record_event(self, event: AnalyticsEvent) -> None:
        metadata = json.dumps(event.metadata, ensure_ascii=True)
        with closing(self._connect()) as conn:
            with conn:
                conn.execute(
                    """
                    INSERT INTO analytics_events (
                        event_name, entity_id, value, metadata_json, created_at
                    )
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (event.event_name, event.entity_id, event.value, metadata, event.created_at),
                )

    def list_events(self, entity_id: str | None = None) -> list[AnalyticsEvent]:
        query = "SELECT * FROM analytics_events"
        params: tuple[str, ...] = ()
        if entity_id:
            query += " WHERE entity_id = ?"
            params = (entity_id,)
        query += " ORDER BY created_at DESC"
        with closing(self._connect()) as conn:
            rows = conn.execute(query, params).fetchall()
        return [
            AnalyticsEvent(
                event_name=row["event_name"],
                entity_id=row["entity_id"],
                value=row["value"],
                metadata=json.loads(row["metadata_json"]),
                created_at=row["created_at"],
            )
            for row in rows
        ]

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def _row_to_opportunity(payload_json: str) -> Opportunity:
        payload = json.loads(payload_json)
        payload["keywords"] = tuple(payload.get("keywords", ()))
        return Opportunity(**payload)
