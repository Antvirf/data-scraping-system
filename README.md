# Data scraping system

## Usage

```bash
make up # bring continuously running services like db and ingestion (ctrl+c to stop)
make initialize # initialize data from local JSON
make collect # scrape and send data for ingestion from available scrapers
make collect-local # scrape and save data locally (json)
make down # remove resources created by compose, including clearing db
```

## Background

Practice and experimentation project to make multi-part application trying out different technologies.

- Database / persistence layer
- Data collector API to periodically get something into the DB
- Internal data ingestion service (interacts with various  DB backends)
- Outbound service API to query
  - REST API
  - GraphQL API
- Some type of Admin UI or similar to view (some) content - using e.g. Strapi or PocketBase connected to the main DB

## Current short-term to-do

1. Build Postgres persistence layer
    1. R of CRUD
    1. D of CRUD
1. Make database reads async (test with simulated delays)
1. Create first external API (Python version)
    1. TDD approach
    1. Read only, but implement a few different methods
    1. Provide OpenAPI/Swagger docs
1. Write tests for ingestion service
1. Write tests for 28hse scraper
1. Start setting up kubernetes installation

## MVP To-do

- ~~Set up in Compose~~
- ~~PostgreSQL, running in the cluster itself~~
- ~~One data collector pod written in Python, pass data to ingestion~~
- ~~Data ingestion service in Python, push data from data collector to PostgreSQL~~
- ~~Basic versioning/changelogs with release please~~
- REST API to fetch scraped data

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
- If a frontend can be SPA, host it on GitHub pages?
- Data pipeline where Python/Airflow crawls data, puts into storage, picked up by Airflow or Spark, reformatted and pushed to DB
- Thorough tests for EVERYTHING

## Components & Architecture

### Scrapers - ```scrapers```

Individual modules built with varying languages, with images that can be configured as kubernetes cronjobs that will collect data and send them via REST calls to ```ingestion```.

### Ingestion - ```ingestion```

A Python FastAPI-based REST API that receives data from all ```scrapers``` and pushes them to a backend database. All interactions with the DB happen here, so ```ingestion``` will also contain database initialization scripts. First backend to be implemented will be PostgreSQL.
