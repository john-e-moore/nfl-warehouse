"""Command-line entry point for fixture-backed market parsing."""

import argparse
import json
from pathlib import Path

from .markets import MarketResponseError, parse_markets_response


def main() -> int:
    parser = argparse.ArgumentParser(description="Parse a Kalshi markets fixture")
    parser.add_argument("--fixture", type=Path, required=True, help="JSON fixture path")
    args = parser.parse_args()

    try:
        with args.fixture.open(encoding="utf-8") as handle:
            records = parse_markets_response(json.load(handle))
    except (OSError, json.JSONDecodeError, MarketResponseError) as exc:
        parser.error(f"could not parse fixture: {exc}")

    print(f"parsed {len(records)} typed market records")
    return 0
