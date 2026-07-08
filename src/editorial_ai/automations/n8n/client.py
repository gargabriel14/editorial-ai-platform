"""n8n webhook adapter."""

from __future__ import annotations

import json
import os
from typing import Any
from urllib import request


class N8NWebhookPublisher:
    """Publish structured platform events to an n8n webhook."""

    def __init__(self, webhook_url: str | None = None, timeout_seconds: int = 20) -> None:
        self.webhook_url = webhook_url or os.getenv("N8N_WEBHOOK_URL", "")
        self.timeout_seconds = timeout_seconds

    def publish(self, event_name: str, payload: dict[str, Any]) -> None:
        if not self.webhook_url:
            raise RuntimeError("N8N_WEBHOOK_URL is not configured.")
        body = json.dumps({"event_name": event_name, "payload": payload}).encode("utf-8")
        req = request.Request(
            self.webhook_url,
            data=body,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with request.urlopen(req, timeout=self.timeout_seconds) as response:
            if response.status >= 400:
                raise RuntimeError(f"n8n webhook failed with HTTP {response.status}")

