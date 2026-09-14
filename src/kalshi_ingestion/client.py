"""Read-only client for the public Kalshi markets endpoint."""

from __future__ import annotations

import json
import os
from typing import Final
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from .markets import MarketRecord, MarketResponseError, parse_markets_response


DEFAULT_API_BASE_URL: Final = "https://external-api.kalshi.com/trade-api/v2"


class KalshiClientError(RuntimeError):
    """Raised when a read-only Kalshi request cannot produce market records."""


class KalshiMarketsClient:
    """Retrieve one validated markets page from Kalshi's public API.

    The endpoint is public, so this client deliberately does not read, sign with,
    or transmit API credentials. Pagination belongs to M1-T3.
    """

    def __init__(self, base_url: str = DEFAULT_API_BASE_URL, timeout_seconds: float = 20.0):
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("Kalshi API base URL must be an absolute HTTP(S) URL")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._base_url = base_url.rstrip("/")
        self._timeout_seconds = timeout_seconds

    @classmethod
    def from_environment(cls) -> KalshiMarketsClient:
        """Build a public client using the optional non-secret base URL setting."""

        return cls(base_url=os.environ.get("KALSHI_API_BASE_URL", DEFAULT_API_BASE_URL))

    def fetch_markets(self, *, series_ticker: str, limit: int = 100) -> list[MarketRecord]:
        """Fetch and validate a single Kalshi markets page for one series."""

        if not series_ticker:
            raise ValueError("series_ticker must not be empty")
        if not 1 <= limit <= 1000:
            raise ValueError("limit must be between 1 and 1000")

        query = urlencode({"series_ticker": series_ticker, "limit": limit})
        request = Request(
            f"{self._base_url}/markets?{query}",
            headers={"Accept": "application/json"},
            method="GET",
        )
        try:
            with urlopen(request, timeout=self._timeout_seconds) as response:
                payload = json.load(response)
        except HTTPError as exc:
            raise KalshiClientError(f"Kalshi markets request returned HTTP {exc.code}") from exc
        except (URLError, OSError) as exc:
            raise KalshiClientError("Kalshi markets request failed") from exc
        except json.JSONDecodeError as exc:
            raise KalshiClientError("Kalshi markets response was not valid JSON") from exc

        try:
            return parse_markets_response(payload)
        except MarketResponseError as exc:
            raise KalshiClientError("Kalshi markets response failed validation") from exc
