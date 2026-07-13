# Hybrid Governance Automation

This repository provides architectural components for automated change gating, ticketing integrations, real-time alert delivery, and project-tracking synchronization. The system establishes non-interactive compliance checkpoints between Continuous Integration engines (**Jenkins**, **Azure DevOps**) and enterprise IT Service Management (ITSM)/Agile Systems (**ServiceNow**, **Azure DevOps Boards**).

## Architecture Highlights
- **Multi-Engine Pipelines:** Uses Azure DevOps for cloud-scale landing zones and SLES/SAP deployments, while utilizing Jenkins for on-premises Tier 1 application node deployment and line-of-sight network orchestration.
- **Automated Guardrails:** Python scripts integrated directly into the CI/CD pipeline to parse API states for ServiceNow Change Requests, preventing unapproved modifications to **PRD/UAT** environments.

## Operational Problem Solved
Manual compliance monitoring scales poorly across decoupled staging boundaries. This package implements software-defined gates to prevent configuration drift, enforce maintenance window validations, and eliminate manual tracking updates across isolated lifecycle layers.

## Technical Framework & Automation Modules
- **Pre-Execution Change Validation (`scripts/servicenow_change_gate.py`):** Python automation queries internal ticketing systems to verify scheduled deployment windows before provisioning compute fabrics.
- **Bi-Directional State Synchronization (`scripts/azdo_board_sync.py`):** Automatic patch mechanics push execution histories directly into parent project tracking layers upon deployment.
- **Multi-Engine Target Profiles:** Native execution pipelines configured for Azure DevOps cloud fabrics and Jenkins on-premises topologies.
- **Dynamic Topological Auditing:** The analytical engine tracks regional metrics, cloud availability zones (`canadaeast`, `canadacentral`), and local virtualization contexts (`ESXi-Cluster-01`).
- **Automated Notification Pathways:** Includes dedicated payload delivery models that intercept verification breakdowns and route warnings directly to messaging webhooks.
- **Priority-Aware Notification Engine (`scripts/send_pipeline_alert.py`):** Evaluates asset threat ratings (Tier0, Tier1, Tier2) and routes critical incidents to emergency engineering endpoints while directing non-critical staging notices to general operations tracking logs.
- **Architectural Policy Control:** Structural governance decisions are preserved via an Architectural Decision Record (ADR) matrix located inside the repository directories.
- **Continuous Compliance Engine (`scripts/generate_compliance_report.py`):** Evaluates multi-cloud and on-premises infrastructure inventories against corporate safety metrics. Captures layout data including regional tags, availability zones, and security perimeters to generate markdown report summaries.
- **Static Security Testing (SAST):** Pipeline integrations run security analysis (`bandit`) checking for hardcoded secrets, injection vectors, or weak cryptography.

## Updated System Architecture Layout
The configuration engine links project boards, pipeline validators, messaging hooks, and inventory matrices into a unified workspace layer:
[ Local Code Updates ] ──► [ Pipeline Linters ] ──► [ Ansible-Lint / Puppet-Lint ]
│
▼ (Success Condition)
[ Runbook Analytics  ] ──► [ Compliance Engine ] ──► [ Markdown Audit Reports ]
│
▼ (Failure Intercept)
[ Operations Teams   ] ◄── [ Notification Hub ] ◄── [ Real-Time Chat Webhooks ]

## Layout Configuration
- **.azure-pipelines/platform-provision-gate.yml:** Native configuration file handling change controls, security lint stages, and automated parameters.
- **.jenkins/Jenkinsfile.deploy:** Declarative pipeline orchestrator targeting local line-of-sight application nodes.
- **docs/adr/:** Directory hosting consolidated Architectural Decision Records (ADRs).

## System Prerequisites
- Python 3.10+
- Execution access to enterprise project platform REST endpoints
