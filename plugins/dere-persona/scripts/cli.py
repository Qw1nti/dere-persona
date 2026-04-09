"""CLI entry point for dere-persona."""

from __future__ import annotations

import argparse
import sys

from settings import load_settings
from transformer import transform_text


def build_parser() -> argparse.ArgumentParser:
    settings = load_settings()
    parser = argparse.ArgumentParser(description="Apply dere-inspired style to prose only.")
    parser.add_argument("--persona", default=settings["default_persona"], help="Persona profile name")
    parser.add_argument("--text", help="Input text. If omitted, stdin is used.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    text = args.text if args.text is not None else sys.stdin.read()
    sys.stdout.write(transform_text(text=text, persona=args.persona))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
