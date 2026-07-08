"""Command line interface for the Editorial AI Platform."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from editorial_ai.core.platform import build_default_platform
from editorial_ai.core.storage import SQLiteOpportunityRepository
from editorial_ai.core.utils import to_jsonable


DEFAULT_SEEDS = (
    "guias de prompts de IA para profesores",
    "habitos de productividad para freelancers",
    "cuadernos mindfulness para adolescentes",
    "sistemas simples de finanzas para creativos",
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="editorial-ai")
    parser.add_argument("--db", default="data/editorial_ai.sqlite", help="SQLite database path.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-db", help="Create local database tables.")
    init_parser.set_defaults(func=_init_db)

    demo_parser = subparsers.add_parser("run-demo", help="Run the full demo pipeline.")
    demo_parser.add_argument("--out", default="outputs/demo", help="Output directory.")
    demo_parser.add_argument("--seed", action="append", help="Seed topic. Can be passed multiple times.")
    demo_parser.set_defaults(func=_run_demo)

    list_parser = subparsers.add_parser("list-opportunities", help="List scored opportunities.")
    list_parser.add_argument("--limit", type=int, default=10)
    list_parser.add_argument("--min-score", type=float, default=0)
    list_parser.set_defaults(func=_list_opportunities)

    args = parser.parse_args(argv)
    return args.func(args)


def _init_db(args: argparse.Namespace) -> int:
    repository = SQLiteOpportunityRepository(args.db)
    repository.setup()
    print(f"Database ready: {args.db}")
    return 0


def _run_demo(args: argparse.Namespace) -> int:
    seeds = tuple(args.seed) if args.seed else DEFAULT_SEEDS
    platform = build_default_platform(args.db)
    result = platform.run_opportunity_pipeline(seeds)
    output = platform.export_result(result, args.out)
    print(f"Pipeline completed with {len(result.opportunities)} opportunities.")
    print(f"Result written to {output}")
    print(json.dumps(to_jsonable(result.opportunities), indent=2, ensure_ascii=True))
    return 0


def _list_opportunities(args: argparse.Namespace) -> int:
    repository = SQLiteOpportunityRepository(args.db)
    repository.setup()
    opportunities = repository.list_opportunities(limit=args.limit, min_score=args.min_score)
    if not opportunities:
        print("No opportunities found.")
        return 0
    for item in opportunities:
        print(f"{item.total_score:5.1f} | {item.id} | {item.title_angle} | {item.status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

