"""Offline construction of immutable raw-output contract v1 artifacts."""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import uuid
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from io import BytesIO

_IDENTIFIER_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}\Z")


class RawArtifactError(ValueError):
    """Raised when artifacts cannot comply with raw-output contract v1."""


@dataclass(frozen=True, slots=True)
class RawResponsePage:
    """A source response captured before decoding, with validated page metadata."""

    response_bytes: bytes
    request_cursor: str | None
    next_cursor: str
    record_count: int


@dataclass(frozen=True, slots=True)
class RawRun:
    """Non-secret run metadata required by the raw-output v1 manifest."""

    run_id: str
    provider: str
    entity: str
    observed_at: datetime
    request_started_at: datetime
    request_completed_at: datetime
    collector_version: str
    git_sha: str
    endpoint: str
    request_parameters: Mapping[str, str]


@dataclass(frozen=True, slots=True)
class RawPayload:
    """One compressed response object that a later writer can publish."""

    key: str
    compressed_bytes: bytes


@dataclass(frozen=True, slots=True)
class RawRunArtifacts:
    """Payloads and manifest bytes ready for create-only persistence."""

    payloads: tuple[RawPayload, ...]
    manifest_key: str
    manifest_bytes: bytes


def _format_timestamp(value: datetime, field_name: str) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise RawArtifactError(f"{field_name} must be timezone-aware")
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _validate_identifier(value: str, field_name: str) -> None:
    if not _IDENTIFIER_PATTERN.fullmatch(value):
        raise RawArtifactError(f"{field_name} must be a lower-case ASCII identifier")


def _validate_run(run: RawRun) -> tuple[str, str, str]:
    _validate_identifier(run.provider, "provider")
    _validate_identifier(run.entity, "entity")
    try:
        parsed_run_id = uuid.UUID(run.run_id)
    except ValueError as exc:
        raise RawArtifactError("run_id must be a canonical lower-case UUID") from exc
    if str(parsed_run_id) != run.run_id:
        raise RawArtifactError("run_id must be a canonical lower-case UUID")
    if not run.collector_version:
        raise RawArtifactError("collector_version must not be empty")
    if not run.git_sha:
        raise RawArtifactError("git_sha must not be empty")
    if not run.endpoint:
        raise RawArtifactError("endpoint must not be empty")
    if any(
        not isinstance(key, str) or not isinstance(value, str)
        for key, value in run.request_parameters.items()
    ):
        raise RawArtifactError("request_parameters must contain only string keys and values")

    observed_at = _format_timestamp(run.observed_at, "observed_at")
    request_started_at = _format_timestamp(run.request_started_at, "request_started_at")
    request_completed_at = _format_timestamp(run.request_completed_at, "request_completed_at")
    if run.request_completed_at < run.request_started_at:
        raise RawArtifactError("request_completed_at must not precede request_started_at")
    return observed_at, request_started_at, request_completed_at


def _gzip_response(response_bytes: bytes) -> bytes:
    destination = BytesIO()
    with gzip.GzipFile(fileobj=destination, mode="wb", filename="", mtime=0) as compressed:
        compressed.write(response_bytes)
    return destination.getvalue()


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _validate_pages(pages: Sequence[RawResponsePage]) -> None:
    if not pages:
        raise RawArtifactError("a successful run must contain at least one response page")
    previous_next_cursor: str | None = None
    for index, page in enumerate(pages):
        if not isinstance(page.response_bytes, bytes):
            raise RawArtifactError("response_bytes must be bytes")
        if not isinstance(page.next_cursor, str):
            raise RawArtifactError("next_cursor must be a string")
        if page.request_cursor is not None and not isinstance(page.request_cursor, str):
            raise RawArtifactError("request_cursor must be a string or null")
        if (
            not isinstance(page.record_count, int)
            or isinstance(page.record_count, bool)
            or page.record_count < 0
        ):
            raise RawArtifactError("record_count must be non-negative")
        if index == 0:
            if page.request_cursor is not None:
                raise RawArtifactError("the first page request_cursor must be null")
        elif page.request_cursor != previous_next_cursor:
            raise RawArtifactError("page request_cursor must match the prior next_cursor")
        if index < len(pages) - 1 and not page.next_cursor:
            raise RawArtifactError("only the final page may have an empty next_cursor")
        previous_next_cursor = page.next_cursor
    if pages[-1].next_cursor:
        raise RawArtifactError("the final page next_cursor must be empty")


def build_raw_run_artifacts(run: RawRun, pages: Sequence[RawResponsePage]) -> RawRunArtifacts:
    """Build deterministic payload and manifest bytes under raw-output contract v1."""

    observed_at, request_started_at, request_completed_at = _validate_run(run)
    _validate_pages(pages)
    observed_datetime = run.observed_at.astimezone(UTC)
    prefix = (
        f"provider={run.provider}/entity={run.entity}/"
        f"observed_date={observed_datetime:%Y-%m-%d}/observed_hour={observed_datetime:%H}/"
        f"run_id={run.run_id}"
    )

    payloads: list[RawPayload] = []
    raw_objects: list[dict[str, object]] = []
    for page_sequence, page in enumerate(pages, start=1):
        compressed_bytes = _gzip_response(page.response_bytes)
        key = f"{prefix}/response-{page_sequence:04d}.json.gz"
        payloads.append(RawPayload(key=key, compressed_bytes=compressed_bytes))
        raw_objects.append(
            {
                "key": key,
                "page_sequence": page_sequence,
                "request_cursor": page.request_cursor,
                "next_cursor": page.next_cursor,
                "record_count": page.record_count,
                "response_bytes": len(page.response_bytes),
                "compressed_bytes": len(compressed_bytes),
                "response_sha256": _sha256(page.response_bytes),
                "compressed_sha256": _sha256(compressed_bytes),
            }
        )

    manifest = {
        "schema_version": "raw-output/v1",
        "run": {
            "run_id": run.run_id,
            "provider": run.provider,
            "entity": run.entity,
            "observed_at": observed_at,
            "request_started_at": request_started_at,
            "request_completed_at": request_completed_at,
            "collector_version": run.collector_version,
            "git_sha": run.git_sha,
            "request": {
                "endpoint": run.endpoint,
                "parameters": dict(run.request_parameters),
            },
        },
        "raw_objects": raw_objects,
        "totals": {
            "raw_object_count": len(raw_objects),
            "record_count": sum(page.record_count for page in pages),
            "response_bytes": sum(len(page.response_bytes) for page in pages),
            "compressed_bytes": sum(len(payload.compressed_bytes) for payload in payloads),
        },
    }
    return RawRunArtifacts(
        payloads=tuple(payloads),
        manifest_key=f"{prefix}/manifest.json",
        manifest_bytes=json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode("utf-8"),
    )
