# NFL warehouse

Local-first Kalshi NFL market extraction primitives. The package supports a
committed fixture mode for offline development and an explicitly selected,
read-only live mode for the public Kalshi markets endpoint.

## Clean checkout

The project targets Python 3.12 or newer. From a fresh checkout:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[dev]'
```

Run the full local verification suite:

```bash
.venv/bin/ruff format --check .
.venv/bin/ruff check .
.venv/bin/mypy
.venv/bin/python -m unittest discover -s tests -v
```

The fixture-backed CLI path requires no network access:

```bash
.venv/bin/kalshi-markets --fixture fixtures/kalshi_markets.json
# parsed 1 typed market records
```

Live retrieval is opt-in and read-only. It requires a public series ticker and
may use `KALSHI_API_BASE_URL` to select a non-secret API base URL:

```bash
.venv/bin/kalshi-markets --live --series-ticker KXNFLGAME
```

The default test suite never requires live access or credentials.

## Development S3 infrastructure

Milestone 2 includes a Terraform root module for a protected development raw
bucket and a constrained writer role. It is separate from the offline package
workflow and does not apply infrastructure automatically. See
[`infra/terraform/development-s3`](infra/terraform/development-s3) for its
review-first configuration and operating instructions. Application persistence
and its authorized read-back demonstration remain the next task.

## Project layout

- `src/kalshi_ingestion/` — typed response validation, client, and CLI
- `fixtures/` — sanitized source-shaped responses used by offline tests
- `tests/` — fixture and local-server tests
- `infra/terraform/development-s3/` — development raw S3 bucket and writer role
- `docs/` — architecture, requirements, and accepted decisions

The current scope is local extraction and development raw-storage provisioning.
Application-level S3 persistence, Snowflake, dbt, scheduling, and additional
providers are intentionally deferred to later milestones.
