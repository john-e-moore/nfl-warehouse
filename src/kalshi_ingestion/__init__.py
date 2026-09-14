"""Typed, local-first Kalshi market extraction."""

from .markets import MarketRecord, parse_markets_response

__all__ = ["MarketRecord", "parse_markets_response"]
