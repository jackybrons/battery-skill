from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import BM25Retriever, ContextBuilder, lint_text, route_query


def cmd_route(args: argparse.Namespace) -> int:
    route = route_query(args.query)
    print(json.dumps({"section": route.section, "domains": route.domains, "journals": route.journals, "needs_terminology": route.needs_terminology, "preferred_paths": route.preferred_paths}, ensure_ascii=False, indent=2))
    return 0


def cmd_retrieve(args: argparse.Namespace) -> int:
    root = Path(args.root or ".").resolve()
    route = route_query(args.query)
    for i, hit in enumerate(BM25Retriever(root).search(args.query, route, k=args.k), 1):
        print(f"[{i}] score={hit.score:.3f} {hit.chunk.path} :: {hit.chunk.heading}\n{hit.chunk.text.strip()}\n")
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    bundle = ContextBuilder(Path(args.root or ".").resolve()).build(args.query, args.k, args.max_chars)
    print(bundle.render(), end="")
    return 0


def cmd_lint(args: argparse.Namespace) -> int:
    import sys
    text = Path(args.path).read_text(encoding="utf-8") if args.path != "-" else sys.stdin.read()
    warnings = lint_text(text)
    if not warnings:
        print("No heuristic warnings.")
        return 0
    for w in warnings:
        print(f"{w.code}: {w.message}")
    return 1 if args.strict else 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="battery-skill")
    sub = p.add_subparsers(dest="command", required=True)
    x = sub.add_parser("route"); x.add_argument("query"); x.set_defaults(func=cmd_route)
    x = sub.add_parser("retrieve"); x.add_argument("query"); x.add_argument("-k", type=int, default=6); x.add_argument("--root"); x.set_defaults(func=cmd_retrieve)
    x = sub.add_parser("context"); x.add_argument("query"); x.add_argument("-k", type=int, default=6); x.add_argument("--max-chars", type=int, default=12000); x.add_argument("--root"); x.set_defaults(func=cmd_context)
    x = sub.add_parser("lint"); x.add_argument("path"); x.add_argument("--strict", action="store_true"); x.set_defaults(func=cmd_lint)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
