"""Command-line entry point for GeoVideo."""

from __future__ import annotations

import argparse
from pathlib import Path

from .config import ProjectConfig


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GeoVideo project helper")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Project root directory")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    config = ProjectConfig.from_root(args.root)
    print(f"Assets directory: {config.assets_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
