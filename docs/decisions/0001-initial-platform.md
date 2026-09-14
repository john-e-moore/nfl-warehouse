# ADR 0001: Initial platform and orchestration

- Status: Accepted
- Date: 2026-09-14

## Context

The project needs a production-capable pipeline for hourly Kalshi NFL market
observations. It should remain inexpensive and understandable for one developer,
while leaving a path to additional providers. Operating a persistent workflow
platform before cross-job dependencies exist would add cost and another system
to maintain.

## Decision

- Use Python for extraction and data-engineering application code.
- Preserve exact compressed JSON responses in Amazon S3 as the raw source of truth.
- Run scheduled extraction and dbt Core workloads as containerized ECS Fargate tasks.
- Use EventBridge Scheduler for initial schedules.
- Load raw data into Snowflake and transform it with dbt Core.
- Use GitHub Actions for testing, image builds, and deployment—not as the production
  hourly scheduler.
- Use CloudWatch metrics/logs and operator notifications for initial observability.
- Defer Airflow and Prefect until multi-provider dependencies, conditional workflows,
  or backfill operations create a demonstrated orchestration need.
- Defer a separate S3 Parquet/silver layer until a concrete consumer or scale need exists.

## Consequences

### Benefits

- Nearly all compute remains usage-based.
- Local and production execution share container boundaries.
- The operator can understand failures without maintaining an orchestration cluster.
- Immutable raw responses allow replay and schema evolution.

### Costs and tradeoffs

- Cross-step lineage initially depends on disciplined run IDs and structured metadata.
- EventBridge and CloudWatch provide less unified workflow visualization than Airflow
  or Prefect.
- Snowflake compute must be scheduled carefully because warehouse resumes have a
  minimum billing interval.
- Future browser-heavy providers may require new technical and legal evaluation.

## Revisit when

- three or more provider pipelines have meaningful dependencies;
- conditional recovery or dynamic backfills become frequent;
- reconstructing one logical run across services becomes operationally expensive;
- another consumer requires a durable Parquet layer;
- hourly capture fails to support the intended research use case.

