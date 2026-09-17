import json
import unittest
from pathlib import Path

from kalshi_ingestion.markets import (
    MarketResponseError,
    parse_markets_page,
    parse_markets_response,
)

FIXTURE = Path(__file__).parents[1] / "fixtures" / "kalshi_markets.json"


class MarketParsingTests(unittest.TestCase):
    def test_valid_fixture_returns_typed_record_and_preserves_unknown_fields(self) -> None:
        with FIXTURE.open(encoding="utf-8") as handle:
            records = parse_markets_response(json.load(handle))

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].ticker, "KXNFLGAME-26SEP13-BUFNYJ-BUF")
        self.assertEqual(records[0].volume, 1842)
        self.assertEqual(records[0].raw["custom_source_field"], "preserved")

    def test_malformed_response_is_rejected(self) -> None:
        with self.assertRaises(MarketResponseError):
            parse_markets_response({"markets": [{"title": "missing ticker"}]})

    def test_empty_terminal_page_has_an_empty_cursor(self) -> None:
        records, cursor = parse_markets_page({"markets": [], "cursor": ""})

        self.assertEqual(records, [])
        self.assertEqual(cursor, "")

    def test_missing_or_non_string_cursor_is_rejected(self) -> None:
        with self.assertRaisesRegex(MarketResponseError, "cursor"):
            parse_markets_page({"markets": []})
        with self.assertRaisesRegex(MarketResponseError, "cursor"):
            parse_markets_page({"markets": [], "cursor": None})


if __name__ == "__main__":
    unittest.main()
