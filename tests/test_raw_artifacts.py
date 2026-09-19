import gzip
import hashlib
import json
import unittest
from datetime import UTC, datetime
from pathlib import Path

from kalshi_ingestion.raw_artifacts import (
    RawArtifactError,
    RawResponsePage,
    RawRun,
    build_raw_run_artifacts,
)

FIXTURE = Path(__file__).parents[1] / "fixtures" / "kalshi_markets.json"
RUN_ID = "123e4567-e89b-12d3-a456-426614174000"


def sample_run(*, run_id: str = RUN_ID) -> RawRun:
    return RawRun(
        run_id=run_id,
        provider="kalshi",
        entity="markets",
        observed_at=datetime(2026, 9, 17, 14, 32, 1, tzinfo=UTC),
        request_started_at=datetime(2026, 9, 17, 14, 31, 59, tzinfo=UTC),
        request_completed_at=datetime(2026, 9, 17, 14, 32, 1, tzinfo=UTC),
        collector_version="0.1.0",
        git_sha="abc123",
        endpoint="/trade-api/v2/markets",
        request_parameters={"limit": "100", "series_ticker": "KXNFLGAME"},
    )


class RawArtifactTests(unittest.TestCase):
    def test_payload_round_trip_preserves_fixture_bytes_and_is_deterministic(self) -> None:
        fixture_bytes = FIXTURE.read_bytes()
        pages = [RawResponsePage(fixture_bytes, None, "", 1)]

        artifacts = build_raw_run_artifacts(sample_run(), pages)
        repeated = build_raw_run_artifacts(sample_run(), pages)

        self.assertEqual(artifacts, repeated)
        self.assertEqual(gzip.decompress(artifacts.payloads[0].compressed_bytes), fixture_bytes)
        self.assertEqual(
            artifacts.payloads[0].key,
            "provider=kalshi/entity=markets/observed_date=2026-09-17/"
            f"observed_hour=14/run_id={RUN_ID}/response-0001.json.gz",
        )

    def test_manifest_has_partition_fields_checksums_and_totals(self) -> None:
        first_page = FIXTURE.read_bytes()
        second_page = b'{"markets":[],"cursor":""}'
        artifacts = build_raw_run_artifacts(
            sample_run(),
            [
                RawResponsePage(first_page, None, "cursor-2", 1),
                RawResponsePage(second_page, "cursor-2", "", 0),
            ],
        )

        manifest = json.loads(artifacts.manifest_bytes)

        self.assertEqual(manifest["schema_version"], "raw-output/v1")
        self.assertEqual(manifest["run"]["observed_at"], "2026-09-17T14:32:01Z")
        self.assertEqual(manifest["run"]["request"]["parameters"]["limit"], "100")
        self.assertEqual(manifest["raw_objects"][0]["request_cursor"], None)
        self.assertEqual(manifest["raw_objects"][1]["next_cursor"], "")
        self.assertEqual(manifest["raw_objects"][0]["key"], artifacts.payloads[0].key)
        self.assertEqual(
            manifest["raw_objects"][0]["response_sha256"], hashlib.sha256(first_page).hexdigest()
        )
        self.assertEqual(
            manifest["raw_objects"][0]["compressed_sha256"],
            hashlib.sha256(artifacts.payloads[0].compressed_bytes).hexdigest(),
        )
        self.assertEqual(
            manifest["totals"],
            {
                "raw_object_count": 2,
                "record_count": 1,
                "response_bytes": len(first_page) + len(second_page),
                "compressed_bytes": sum(
                    len(payload.compressed_bytes) for payload in artifacts.payloads
                ),
            },
        )
        self.assertEqual(
            artifacts.manifest_key,
            "provider=kalshi/entity=markets/observed_date=2026-09-17/"
            f"observed_hour=14/run_id={RUN_ID}/manifest.json",
        )

    def test_run_id_makes_object_names_collision_safe(self) -> None:
        pages = [RawResponsePage(b'{"markets":[],"cursor":""}', None, "", 0)]
        first = build_raw_run_artifacts(sample_run(), pages)
        second = build_raw_run_artifacts(
            sample_run(run_id="123e4567-e89b-12d3-a456-426614174001"), pages
        )

        self.assertNotEqual(first.payloads[0].key, second.payloads[0].key)
        self.assertNotEqual(first.manifest_key, second.manifest_key)

    def test_rejects_nonterminal_cursor_and_noncanonical_run_id(self) -> None:
        with self.assertRaisesRegex(RawArtifactError, "final page"):
            build_raw_run_artifacts(sample_run(), [RawResponsePage(b"{}", None, "next", 0)])
        with self.assertRaisesRegex(RawArtifactError, "canonical"):
            build_raw_run_artifacts(
                sample_run(run_id=RUN_ID.upper()), [RawResponsePage(b"{}", None, "", 0)]
            )


if __name__ == "__main__":
    unittest.main()
