"""Validation and typed representation for a Kalshi markets response."""

from dataclasses import dataclass
from typing import Any, Mapping


class MarketResponseError(ValueError):
    """Raised when a markets response does not match the expected envelope."""


@dataclass(frozen=True, slots=True)
class MarketRecord:
    """The minimum typed market representation needed by M1-T1.

    Timestamp values stay as source strings until a later boundary can define
    the required normalization and timezone behavior. ``raw`` retains the
    complete source market mapping, including fields not modeled here.
    """

    ticker: str
    event_ticker: str
    series_ticker: str | None
    title: str
    subtitle: str | None
    status: str
    open_time: str | None
    close_time: str | None
    expiration_time: str | None
    created_time: str | None
    updated_time: str | None
    yes_bid: int | None
    yes_ask: int | None
    no_bid: int | None
    no_ask: int | None
    last_price: int | None
    volume: int | None
    open_interest: int | None
    rules_primary: str | None
    raw: Mapping[str, Any]


def _optional_string(market: Mapping[str, Any], name: str) -> str | None:
    value = market.get(name)
    if value is not None and not isinstance(value, str):
        raise MarketResponseError(f"market field {name!r} must be a string or null")
    return value


def _optional_integer(market: Mapping[str, Any], name: str) -> int | None:
    value = market.get(name)
    if value is not None and (not isinstance(value, int) or isinstance(value, bool)):
        raise MarketResponseError(f"market field {name!r} must be an integer or null")
    return value


def parse_markets_response(payload: object) -> list[MarketRecord]:
    """Validate one Kalshi markets envelope and return its typed records."""

    records, _ = parse_markets_page(payload)
    return records


def parse_markets_page(payload: object) -> tuple[list[MarketRecord], str]:
    """Validate a markets page and return its records with the next cursor."""

    if not isinstance(payload, dict):
        raise MarketResponseError("response must be a JSON object")
    markets = payload.get("markets")
    if not isinstance(markets, list):
        raise MarketResponseError("response field 'markets' must be a list")
    cursor = payload.get("cursor")
    if not isinstance(cursor, str):
        raise MarketResponseError("response field 'cursor' must be a string")

    records: list[MarketRecord] = []
    for index, candidate in enumerate(markets):
        if not isinstance(candidate, dict):
            raise MarketResponseError(f"market at index {index} must be an object")
        for required in ("ticker", "event_ticker", "title", "status"):
            if not isinstance(candidate.get(required), str) or not candidate[required]:
                raise MarketResponseError(
                    f"market at index {index} requires non-empty string field {required!r}"
                )

        records.append(
            MarketRecord(
                ticker=candidate["ticker"],
                event_ticker=candidate["event_ticker"],
                series_ticker=_optional_string(candidate, "series_ticker"),
                title=candidate["title"],
                subtitle=_optional_string(candidate, "subtitle"),
                status=candidate["status"],
                open_time=_optional_string(candidate, "open_time"),
                close_time=_optional_string(candidate, "close_time"),
                expiration_time=_optional_string(candidate, "expiration_time"),
                created_time=_optional_string(candidate, "created_time"),
                updated_time=_optional_string(candidate, "updated_time"),
                yes_bid=_optional_integer(candidate, "yes_bid"),
                yes_ask=_optional_integer(candidate, "yes_ask"),
                no_bid=_optional_integer(candidate, "no_bid"),
                no_ask=_optional_integer(candidate, "no_ask"),
                last_price=_optional_integer(candidate, "last_price"),
                volume=_optional_integer(candidate, "volume"),
                open_interest=_optional_integer(candidate, "open_interest"),
                rules_primary=_optional_string(candidate, "rules_primary"),
                raw=candidate,
            )
        )
    return records, cursor
