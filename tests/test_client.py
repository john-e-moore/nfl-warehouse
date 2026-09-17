import json
import unittest
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from kalshi_ingestion.client import KalshiClientError, KalshiMarketsClient

FIXTURE = Path(__file__).parents[1] / "fixtures" / "kalshi_markets.json"


@contextmanager
def local_server(responses: list[tuple[int, str]]) -> Iterator[tuple[str, list[str]]]:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802 - required by BaseHTTPRequestHandler
            self.server.request_paths.append(self.path)  # type: ignore[attr-defined]
            status, body = self.server.responses[len(self.server.request_paths) - 1]  # type: ignore[attr-defined]
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(body.encode())

        def log_message(self, format: str, *args: object) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.request_paths = []  # type: ignore[attr-defined]
    server.responses = responses  # type: ignore[attr-defined]
    thread = Thread(target=server.serve_forever)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}", server.request_paths  # type: ignore[attr-defined]
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


class KalshiMarketsClientTests(unittest.TestCase):
    def test_fetches_one_page_and_uses_the_existing_parser(self) -> None:
        with FIXTURE.open(encoding="utf-8") as handle:
            body = json.dumps(json.load(handle))

        with local_server([(200, body)]) as (base_url, _):
            records = KalshiMarketsClient(base_url).fetch_markets(
                series_ticker="KXNFLGAME", limit=25
            )

        self.assertEqual(records[0].ticker, "KXNFLGAME-26SEP13-BUFNYJ-BUF")

    def test_live_request_uses_series_and_limit_query_parameters(self) -> None:
        with local_server([(200, '{"markets": [], "cursor": ""}')]) as (base_url, request_paths):
            client = KalshiMarketsClient(base_url)
            self.assertEqual(client.fetch_markets(series_ticker="KXNFLGAME", limit=25), [])

        request = urlparse(request_paths[0])
        self.assertEqual(request.path, "/markets")
        self.assertEqual(parse_qs(request.query), {"series_ticker": ["KXNFLGAME"], "limit": ["25"]})

    def test_http_error_does_not_expose_response_body(self) -> None:
        with local_server([(401, '{"detail":"private response text"}')]) as (base_url, _):
            with self.assertRaisesRegex(KalshiClientError, "HTTP 401") as error:
                KalshiMarketsClient(base_url).fetch_markets(series_ticker="KXNFLGAME")

        self.assertNotIn("private response text", str(error.exception))

    def test_fetches_all_pages_and_sends_each_cursor_once(self) -> None:
        with FIXTURE.open(encoding="utf-8") as handle:
            first_page = json.load(handle)
        first_page["cursor"] = "next page"
        second_market = {**first_page["markets"][0], "ticker": "KXNFLGAME-26SEP20-NEPIT-NE"}
        second_page = {"markets": [second_market], "cursor": ""}

        with local_server([(200, json.dumps(first_page)), (200, json.dumps(second_page))]) as (
            base_url,
            request_paths,
        ):
            records = KalshiMarketsClient(base_url).fetch_markets(
                series_ticker="KXNFLGAME", limit=25
            )

        self.assertEqual(
            [record.ticker for record in records],
            ["KXNFLGAME-26SEP13-BUFNYJ-BUF", "KXNFLGAME-26SEP20-NEPIT-NE"],
        )
        self.assertEqual(len(request_paths), 2)
        self.assertEqual(
            parse_qs(urlparse(request_paths[0]).query),
            {"series_ticker": ["KXNFLGAME"], "limit": ["25"]},
        )
        self.assertEqual(
            parse_qs(urlparse(request_paths[1]).query),
            {"series_ticker": ["KXNFLGAME"], "limit": ["25"], "cursor": ["next page"]},
        )

    def test_empty_terminal_page_returns_no_records(self) -> None:
        with local_server([(200, '{"markets": [], "cursor": ""}')]) as (base_url, request_paths):
            records = KalshiMarketsClient(base_url).fetch_markets(series_ticker="KXNFLGAME")

        self.assertEqual(records, [])
        self.assertEqual(len(request_paths), 1)

    def test_invalid_cursor_envelope_fails_validation(self) -> None:
        with local_server([(200, '{"markets": [], "cursor": null}')]) as (base_url, _):
            with self.assertRaisesRegex(KalshiClientError, "failed validation"):
                KalshiMarketsClient(base_url).fetch_markets(series_ticker="KXNFLGAME")

    def test_repeated_cursor_does_not_look_like_a_complete_retrieval(self) -> None:
        body = '{"markets": [], "cursor": "again"}'
        with local_server([(200, body), (200, body)]) as (base_url, _):
            with self.assertRaisesRegex(KalshiClientError, "cursor repeated"):
                KalshiMarketsClient(base_url).fetch_markets(series_ticker="KXNFLGAME")

    def test_environment_base_url_is_optional_and_non_secret(self) -> None:
        with patch.dict(
            "os.environ", {"KALSHI_API_BASE_URL": "http://example.test/v2"}, clear=True
        ):
            client = KalshiMarketsClient.from_environment()

        self.assertEqual(client._base_url, "http://example.test/v2")


if __name__ == "__main__":
    unittest.main()
