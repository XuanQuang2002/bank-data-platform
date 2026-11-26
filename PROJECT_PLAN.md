# Project Plan: Real-time Banking Data Platform

## Goal
Show hands-on skills that match the Techcombank Data Engineer JD, using public or synthetic data.
Techcombank's real data is not public, so the architecture and engineering quality are the point.

## Story
A retail bank needs real-time transaction monitoring (velocity and fraud rules) and a trusted warehouse
for Customer 360, daily balances and risk reporting, exposed through APIs.

## Datasets
| Role | Dataset |
|---|---|
| Core banking tables (clients, accounts, transactions, loans, cards) | Berka (PKDD'99 Czech bank) |
| High-volume transactions with fraud labels | PaySim and/or IEEE-CIS Fraud Detection |
| Credit risk mart (optional) | Home Credit or Lending Club |
| Reference data | Frankfurter exchange-rate API, generated merchant/branch dimension |

Berka timestamps are from the 1990s, so a replay script shifts them to "now" and inserts them at a configurable rate.

## Architecture
1. Transaction API (FastAPI or Spring Boot): accepts payments, writes to Postgres, uses idempotency keys and the outbox pattern.
2. CDC: Debezium streams Postgres changes to Kafka (Avro + Schema Registry), keyed by `account_id`, with a dead-letter topic.
3. Streaming: Spark Structured Streaming (Scala) for bronze ingestion and windowed aggregates; Flink for fraud rules (optional).
4. Lakehouse: MinIO + Delta/Iceberg with bronze, silver and gold layers, Hive Metastore as catalog.
5. Batch ELT: PySpark (plus at least one Scala job) for cleansing, dedupe and MERGE upserts.
6. Warehouse: dbt star schema with `fact_transaction`, `dim_customer` (SCD2), `dim_account`, `dim_date`, and marts for Customer 360 and daily balances.
7. Orchestration: Airflow with retries, SLAs, sensors and backfills.
8. Quality and serving: Great Expectations or Soda with a quarantine table; FastAPI endpoints; Grafana dashboards.
9. Platform: Docker Compose, then Kubernetes + Helm, Terraform on one cloud, GitHub Actions CI/CD.

## JD requirement -> evidence
| Requirement | Evidence in the project |
|---|---|
| Python, Scala or Java | Python (Airflow, PySpark, FastAPI) and Scala (Spark jobs) |
| Spark, Kafka, Flink, Hadoop | Spark batch and streaming, Kafka + Debezium, optional Flink, Hive Metastore + Delta/Iceberg |
| Build and optimize ETL/ELT at scale | Benchmarks on 50-100M rows with before/after numbers |
| SQL, data modelling, warehousing | Star schema, SCD2, incremental dbt models |
| Distributed systems, microservices, APIs | Transaction service, outbox pattern, idempotent consumers, consumer lag handling |
| Git, CI/CD, best practices | PRs, GitHub Actions, unit + integration tests, ADRs |
| Analytical and debugging skills | Written incident notes (schema drift, late events, data skew) |
| Agile | GitHub Projects, 1-week sprints, user stories with acceptance criteria |
| Nice-to-have: Databricks, Airflow, Snowflake, Docker, K8s, cloud | Airflow, Docker, K8s (kind), Terraform on one cloud, Databricks optional |

## Phases (about 8 weeks, 1-week sprints)

**Phase 0: Foundation (days 1-3).** Git repo, trunk-based flow, docker-compose skeleton (add services gradually), GitHub Projects backlog, CI with lint and a trivial test.
Done when: `docker compose up` starts the stack and CI is green.

**Phase 1: Core banking data (week 1).** Load Berka into Postgres, write the replay script.
Done when: the replayer inserts about 100 tx/sec and the rate is a flag.

**Phase 2: Transaction service (week 2).** `POST /transfers`, `GET /accounts/{id}/transactions`, idempotency keys, outbox pattern, tests with Testcontainers.
Done when: retrying the same request never double-posts, and a test proves it.

**Phase 3: CDC and Kafka (week 3).** Debezium to Kafka with Avro, dead-letter topic, idempotent consumer.
Done when: killing and restarting a consumer loses and duplicates nothing.

**Phase 4: Streaming with Spark (week 4).** Scala Structured Streaming to bronze with checkpointing; windowed spend per account with watermarks.
Done when: a restart resumes from the checkpoint and late events are handled.

**Phase 5: Lakehouse and batch ELT (week 5).** Bronze to silver (dedupe, types, MERGE), silver to gold, Hive Metastore.
Done when: re-running a job for the same day gives identical output.

**Phase 6: Warehouse and orchestration (week 6).** dbt star schema and SCD2, Airflow DAGs, data quality checks with quarantine.
Done when: one command backfills a week of data.

**Phase 7: Fraud rules with Flink (week 7, optional).** More than N transactions in 5 minutes, or a large amount after long inactivity, publishes to `fraud-alerts`. Skip if short on time and say so.

**Phase 8: Performance tuning (week 7).** Run on 50-100M PaySim rows. Change one thing at a time (partitioning, file size, broadcast join, salting, AQE, compaction) and record the effect.
Done when: there is a before/after benchmark table.

**Phase 9: Platform and delivery (week 8).** GitHub Actions (lint, tests, dbt build, image build), API on kind with Helm, Terraform deploy then destroy, Grafana for lag, job duration and freshness.

## Docs that matter most
- 3 to 5 ADRs, for example "Outbox instead of dual writes" and "Iceberg instead of plain Parquet".
- 3 incident notes caused on purpose and fixed: schema change mid-stream, late-arriving events, data skew. Format: symptom, root cause, fix, prevention.
- A benchmark table from Phase 8.
- A 3-minute demo video: payment through the API, then dashboard, then a fraud alert.

## Rules of thumb
- Build a thin end-to-end slice first, then deepen it.
- Only keep a tool if you can explain why it is there. If time is short, cut Flink and Snowflake first.
- Measure everything (rows/sec, latency, runtime) and put numbers on the CV.
- A project does not replace the "3+ years" requirement, but it can help at the interview stage and for junior or mid-level roles.
