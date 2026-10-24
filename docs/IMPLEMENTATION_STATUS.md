# Implementation Status

## Implemented and Tested

- Git and GitHub source control
- Dockerized demo storefront
- Jenkins CI/CD pipeline
- Trivy scan of the application image
- Terraform configuration validation and plan
- Ansible application/container verification
- Kubernetes deployment using Kind
- Helm chart validation and local release installation
- Prometheus and Grafana local monitoring
- Loki and Alloy centralized Docker logging
- Application HTTP logs visible in Grafana Explore

## Scope Limitations

- The storefront is a frontend demo without a real backend or database.
- Kubernetes runs locally using Kind.
- Terraform was validated and planned; successful application of the plan
  has not been established.
- The Trivy result applies only to the image and scan performed.
- Loki and Alloy do not constitute a separate ELK/Kibana implementation.
- The Kubernetes Secret is for demonstration, not production security.
- Cloud deployment has not been verified.

## Pending

- Elasticsearch, Logstash, and Kibana, if required by the project guidelines
- AI-assisted incident analysis
- Cloud deployment
- Final end-to-end verification
- Final project report and complete submission evidence

## Evidence to Capture

- Jenkins successful pipeline
- Docker container status and HTTP health check
- Trivy scan output
- Terraform validation and plan
- Ansible successful playbook output
- Kubernetes resources and Helm release
- Prometheus targets and Grafana monitoring
- Grafana Explore showing application logs from Loki
