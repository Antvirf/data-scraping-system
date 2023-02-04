# Data scraping system

0. Base makefile with dependencies installation automation
1. Makefile configure option to set keys etc.
2. Base makefile, ability to spin up infra from scratch - choose between local or a cloud provider
3. Terraform for Linode, AWS, Azure, GCP
4. Deploy application to multiple envs

## At the base of it: Make a 3 part application that serves some data

- Data collector API to periodically get something into the DB (Python or Go)
- DB
- Internal data transformer microservice (interacts with various  DB backends) (Spring, Python)
- Outbound service API to query (Go?)
  - REST API
  - GraphQL API
- Some type of Admin UI for content - e.g. Can I make Strapi work for this? (JS based) or can I make use of PocketBase?

## MVP

- Running on local Kubernetes
- PostgreSQL, running in the cluster itself
- One data collector pod, push data to local PostgreSQL
- Data transformer microservice in Python

## Planned features / NFRs todo

- Following 12-factor app principles (primarily, separate config)
- Using GHCR
- Automated docs and architecture diagrams?
- Protobuf gRPC between internal data - external data
- GraphQL for external API
- REST for external API
- DevSecOps
- Scalability - HorizontalPodAutoscaler (HPA)
- Scalability - ClusterAutoScaler
- Monitoring, tracing and logging stack installed on the cluster - loki, prometheus, grafana
- OAuth2 proxy (or not; depends on DNS)
- Service mesh
- Kubernetes RBAC configs
- Application performance analytics tooling?
- Kubernetes dashboard
- Data pipeline where Python/Airflow crawls data, puts into storage, picked up by Airflow or Spark, reformatted and pushed to DB
- Thorough tests for EVERYTHING
