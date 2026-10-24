# Project Architecture

## Overview

The project demonstrates a local DevOps workflow for a demo e-commerce
frontend. GitHub stores source code and configuration. Jenkins automates
application validation, image building, scanning, deployment, and health
checks.

## Application Delivery

1. Source code is maintained in GitHub.
2. Jenkins checks out the repository and runs pipeline stages.
3. Docker builds the application image.
4. Trivy scans the image.
5. The configured pipeline deploys a container and checks application health.
6. Kubernetes and Helm provide local orchestration and release management.

## Kubernetes

The local Kind cluster is named `ecommerce-cluster`. The application
namespace is `ecommerce`.

The Kubernetes configuration includes Deployments, Services, a ConfigMap,
and a demonstration Secret. Application deployments use two replicas and
include health probes and resource settings.

## Monitoring

Prometheus collects metrics from configured targets. Grafana provides
metric exploration, dashboards, and alert-rule management.

## Centralized Logging

Grafana Alloy discovers Docker containers and forwards container logs to
Grafana Loki. Grafana Explore queries the logs using LogQL.

Configuration is stored in:

- `logging/alloy/config.alloy`
- `logging/loki/loki-config.yaml`

Application HTTP logs have been observed in Grafana Explore, and Loki's
readiness endpoint returned HTTP 200 in the latest verification.

## Limitations

This describes a local development environment. A separate
Elasticsearch/Logstash/Kibana stack, AI-assisted incident analysis, and
cloud deployment remain pending implementation and verification.
