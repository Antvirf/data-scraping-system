# Data scraping system

Practice project to make a 5 part application:

- Database / persistence layer
- Data collector API to periodically get something into the DB
- Internal data ingestion service (interacts with various  DB backends)
- Outbound service API to query
  - REST API
  - GraphQL API
- Some type of Admin UI or similar to view (some) content - using e.g. Strapi or PocketBase connected to the main DB

## Current short-term to-do

1. Build Postgres persistence layer
  R of CRUD
  D of CRUD
2. Make database reads async somehow - test with delays
3. Create first external API (Python version)
  TEST DRIVEN DEVELOPMENT HERE! Write the tests first.
  Read only, but implement a few different methods
  Provide OpenAPI/Swagger docs
4. Write tests for ingestion service
5. Write tests for 28hse scraper
6. Start setting up kubernetes installation

## MVP To-do

[x] Set up in Compose
[x] PostgreSQL, running in the cluster itself
[x] One data collector pod written in Python, pass data to ingestion
[x] Data ingestion service in Python, push data from data collector to PostgreSQL
[ ] REST API to fetch scraped data

## Various planned features and NFRs in no particular order

- Manage deps and infra setup with Makefile
- Manage secrets with Make for initial config
- Make -> Terraform to provision infra to different providers (potentially Azure / AWS / GCP / Linode)
- Following 12-factor app principles
- Automated performance tests for each component
- Multiple envs (dev sit prod) + automated promotion based on e.g. performance tests
- Using GHCR to upload all images
- Automated docs and architecture diagrams where possible
- Protobuf gRPC between internal data - external data (scrapers -> ingestion)
- GraphQL version for external API
- REST version for external API
- DevSecOps
- Scalability - HorizontalPodAutoscaler (HPA)
- Scalability - ClusterAutoScaler
- Monitoring, tracing and logging stack installed on the cluster - loki, prometheus, grafana
- Service mesh with Istio
- OAuth2 proxy (or not; depends on DNS)
- Kubernetes RBAC configs
- Application performance analytics tooling
- Kubernetes dashboard
- Data pipeline where Python/Airflow crawls data, puts into storage, picked up by Airflow or Spark, reformatted and pushed to DB
- Thorough tests for EVERYTHING

## Components & Architecture

### Scrapers - ```scrapers```

Individual modules built with varying languages, with images that can be configured as kubernetes cronjobs that will collect data and send them via REST calls to ```ingestion```.

### Ingestion - ```ingestion```

A Python FastAPI-based REST API that receives data from all ```scrapers``` and pushes them to a backend database. All interactions with the DB happen here, so ```ingestion``` will also contain database initialization scripts. First backend to be implemented will be PostgreSQL.
