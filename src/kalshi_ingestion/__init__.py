"""Typed, local-first Kalshi market extraction."""

from .client import KalshiMarketsClient
from .markets import MarketRecord, parse_markets_response

__all__ = ["KalshiMarketsClient", "MarketRecord", "parse_markets_response"]
