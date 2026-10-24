# AI-Powered E-Commerce DevOps & Cloud-Native Delivery Platform

## Project Overview

This project demonstrates DevOps practices for a containerized e-commerce
frontend. It includes CI/CD automation, security scanning, infrastructure
automation, Kubernetes, monitoring, and centralized logging.

The storefront is a demo application, not a production e-commerce system.
It does not implement a real backend, persistent database, authentication,
or payment processing.

## Technology Stack

- Linux, Git and GitHub
- Docker and Docker Compose
- Jenkins CI/CD
- Trivy security scanning
- Terraform and Ansible
- Kubernetes with Kind
- Helm
- Prometheus and Grafana
- Grafana Loki and Alloy

## Repository Structure

- `application/` - demo storefront
- `docker/` - Dockerfile and Docker Compose configuration
- `Jenkinsfile` - CI/CD pipeline
- `terraform/` - Terraform configuration
- `ansible/` - application verification playbook
- `kubernetes/` - Kubernetes manifests
- `helm/ecommerce/` - Helm chart
- `monitoring/` - monitoring configuration
- `logging/` - Loki and Alloy configuration
- `docs/` - project documentation

## Run the Application

From the repository root:

    docker compose -f docker/docker-compose.yml up -d --build

Open http://localhost:8082.

Verify the application:

    curl -I http://localhost:8082

Expected response: HTTP 200 OK.

## CI/CD and Security

The Jenkins pipeline is defined in `Jenkinsfile`. Its configured stages
include source checkout, validation, Docker image building, Trivy scanning,
deployment, and application health verification.

Jenkins: http://localhost:8080

The `ai-ecommerce-devops:1.1` image was scanned with Trivy, and the recorded
scan reported zero vulnerabilities within that scan's scope.

## Kubernetes and Helm

The local Kind cluster is `ecommerce-cluster`. The application namespace
is `ecommerce`.

Inspect Kubernetes resources:

    kubectl get all -n ecommerce

Inspect Helm releases:

    helm list -n ecommerce

The deployment includes two replicas per deployment, health probes, resource
settings, a ConfigMap, and a demonstration Secret.

The demo Secret is not a production secret-management solution.

## Terraform and Ansible

Validate Terraform:

    cd terraform
    terraform fmt -check
    terraform validate
    terraform plan
    cd ..

Review the Terraform plan before applying changes. The recorded plan showed
one Docker image resource to create; a successful plan does not mean it was
applied.

Run the Ansible verification playbook:

    ansible-playbook -i localhost, -c local ansible/verify.yml

The playbook previously passed all five tasks without failures.

## Monitoring

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

Prometheus targets and system metrics have been checked in the local
environment. Grafana has been used to inspect CPU, memory, and disk metrics.

## Centralized Logging

Loki stores and queries logs. Alloy discovers Docker containers and forwards
their logs to Loki. Grafana Explore is used to query the collected logs.

Configuration files:

- `logging/loki/loki-config.yaml`
- `logging/alloy/config.alloy`

Check Loki readiness:

    curl -i http://localhost:3100/ready

Example LogQL query:

    {job="docker", container="ai-ecommerce-jenkins"}

Application HTTP logs have been observed in Grafana Explore. Loki 3.5.1
returned HTTP 200 from its readiness endpoint in the latest verification.

This Loki and Alloy setup is not a substitute for a separate
Elasticsearch, Logstash, and Kibana (ELK) implementation.

## Implementation Status

| Component | Status |
|---|---|
| Git and GitHub | Implemented |
| Demo storefront and Docker | Implemented and tested |
| Jenkins CI/CD | Executed successfully |
| Trivy | Application image scanned |
| Terraform | Configuration validated and plan reviewed |
| Ansible | Verification playbook passed |
| Kubernetes with Kind | Deployment tested |
| Helm | Chart validated and release installed |
| Prometheus and Grafana | Configured and tested locally |
| Loki and Alloy | Application logs verified |
| Elasticsearch, Logstash, and Kibana | Pending |
| AI-assisted incident analysis | Pending implementation and verification |
| Cloud deployment | Pending implementation and verification |
| Final submission report | Pending |

## Limitations and Future Work

This is a local development demonstration, not a production deployment.
Cloud deployment, AI-assisted incident analysis, and the separate ELK/Kibana
stack must be implemented and tested before they can be reported as complete.

Further work includes completing the remaining required components,
documenting troubleshooting procedures, and preparing the final report.

## Repository

https://github.com/RRavi20/ai-ecommerce-devops
