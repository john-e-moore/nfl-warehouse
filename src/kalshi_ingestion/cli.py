"""Command-line entry point for fixture or read-only live market retrieval."""

import argparse
import json
from pathlib import Path

from .client import KalshiClientError, KalshiMarketsClient
from .markets import MarketResponseError, parse_markets_response


def main() -> int:
    parser = argparse.ArgumentParser(description="Retrieve or parse Kalshi markets")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture", type=Path, help="JSON fixture path")
    source.add_argument("--live", action="store_true", help="use the public read-only API")
    parser.add_argument("--series-ticker", help="Kalshi series ticker (required with --live)")
    parser.add_argument("--limit", type=int, default=100, help="live page size (1-1000; default: 100)")
    args = parser.parse_args()

    try:
        if args.fixture:
            with args.fixture.open(encoding="utf-8") as handle:
                records = parse_markets_response(json.load(handle))
        else:
            if not args.series_ticker:
                parser.error("--series-ticker is required with --live")
            records = KalshiMarketsClient.from_environment().fetch_markets(
                series_ticker=args.series_ticker,
                limit=args.limit,
            )
    except (OSError, json.JSONDecodeError, MarketResponseError) as exc:
        parser.error(f"could not parse fixture: {exc}")
    except (KalshiClientError, ValueError) as exc:
        parser.error(f"could not retrieve live markets: {exc}")

    print(f"parsed {len(records)} typed market records")
    return 0
