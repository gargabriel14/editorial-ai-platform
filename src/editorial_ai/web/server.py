"""Small stdlib web server for the local dashboard."""

from __future__ import annotations

import json
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from editorial_ai.core.defaults import DEFAULT_SEED_TOPICS
from editorial_ai.web.dashboard import build_dashboard_data, run_demo_and_build_dashboard


PROJECT_ROOT = Path(__file__).resolve().parents[3]
STATIC_DIR = PROJECT_ROOT / "web"


class EditorialDashboardHandler(SimpleHTTPRequestHandler):
    def __init__(
        self,
        *args,
        db_path: str | Path,
        output_dir: str | Path,
        static_dir: str | Path = STATIC_DIR,
        **kwargs,
    ) -> None:
        self.db_path = Path(db_path)
        self.output_dir = Path(output_dir)
        super().__init__(*args, directory=str(static_dir), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            self._send_json({"status": "ok"})
            return
        if parsed.path == "/api/dashboard":
            query = parse_qs(parsed.query)
            limit = _to_int(query.get("limit", ["25"])[0], 25)
            min_score = _to_float(query.get("min_score", ["0"])[0], 0)
            self._send_json(build_dashboard_data(self.db_path, limit=limit, min_score=min_score))
            return
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path != "/api/run-demo":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown API endpoint")
            return
        try:
            payload = self._read_json_body()
            seed_topics = payload.get("seed_topics") or DEFAULT_SEED_TOPICS
            data = run_demo_and_build_dashboard(self.db_path, self.output_dir, seed_topics)
        except Exception as exc:  # pragma: no cover - exercised through browser/server runs
            self._send_json({"error": str(exc)}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
            return
        self._send_json(data)

    def log_message(self, format: str, *args) -> None:
        print(f"[web] {self.address_string()} - {format % args}")

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode("utf-8"))

    def _send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(payload, ensure_ascii=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


def run_server(
    host: str = "127.0.0.1",
    port: int = 8765,
    db_path: str | Path = "data/editorial_ai.sqlite",
    output_dir: str | Path = "outputs/demo",
) -> None:
    handler = partial(
        EditorialDashboardHandler,
        db_path=db_path,
        output_dir=output_dir,
        static_dir=STATIC_DIR,
    )
    server = ThreadingHTTPServer((host, port), handler)
    url = f"http://{host}:{port}"
    print(f"Editorial AI dashboard running at {url}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dashboard.")
    finally:
        server.server_close()


def _to_int(value: str, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _to_float(value: str, fallback: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return fallback

