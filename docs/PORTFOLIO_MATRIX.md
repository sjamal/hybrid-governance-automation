# Hybrid-Cloud Automation & Governance Architecture Dashboard

A production-grade collection of automated deployment frameworks, infrastructure validation utilities, continuous compliance scanners, and edge-ingress orchestrations designed for regulated multi-tenant environments.

The repositories form a logical path that mirrors an enterprise infrastructure lifecycle: Validate Change Window \(\rightarrow \) Provision Node \(\rightarrow \) Apply Declarative Compliance Policies \(\rightarrow \) Build Keystores \(\rightarrow \) Verify Perimeter Boundaries.

---

## 🏗️ Core Structural Topologies

[ ITSM / Audit Logging ] ──► hybrid-governance-automation   (Gating & Alerts)
│
▼
[ Provisioning Handoff ] ──► enterprise-hybrid-pipelines    (Ansible Bootstrap)
│
▼
[ Policy Enforcement  ] ──► puppet-sles-hardening          (OS CIS Compliance)
──► puppet-enterprise-profiles     (Observability Engine)
│
▼
[ Ingress & Edge Tiers ] ──► enterprise-cert-cryptographer  (Keystore Brokers)
──► enterprise-network-mesh        (Boundary Audits)

---

## 📁 Repository Directory Matrix

### 1. hybrid-governance-automation
- **Core Function:** Implements automated ITSM gates, dynamic diagnostic loggers, and priority-weighted alerting pipelines.
- **Key Modules:** `servicenow_change_gate.py`, `send_pipeline_alert.py`, `validate_global_syntax.py`.
- **Validation Layers:** Runs static analysis platforms (`bandit`) paired with local pre-commit hook engines.

### 2. enterprise-hybrid-pipelines
- **Core Function:** Orchestrates hardware post-provisioning baseline structures and system handoffs.
- **Key Modules:** `bootstrap_vms.yml`, `preflight_vss_wrapper.sh`, `sandbox_verification_workbook.yml`.
- **Validation Layers:** Implements independent `keyvault-sync-validation.yml` connection workflows and `ansible-lint` gates.

### 3. puppet-sles-hardening
- **Core Function:** Standalone Puppet 8 configuration module implementing security compliance for SLES 15 hosting SAP/DB2 platforms.
- **Key Modules:** `kernel_tuning.pp`, `system_access.pp`, `workload_profile.pp`.
- **Validation Layers:** Integrates automated parsing Dry-Runs (`puppet parser validate`) and style checker runs.

### 4. puppet-enterprise-profiles
- **Core Function:** Configures shared application components, proxy settings, and Prometheus metrics daemons.
- **Key Modules:** `ingress_observability.pp`, `validate_puppet_resources.py`, `Caddyfile.erb`.
- **Validation Layers:** Restricts environmental definitions via regex-driven manifest validation scripts.

### 5. enterprise-cert-cryptographer
- **Core Function:** Functions as a centralized certificate transformation engine for diverse middleware runtimes.
- **Key Modules:** `cert_broker.py`, `format_converter.sh`, `test_keystore_generation.sh`, `purge_pipeline_artifacts.sh`.
- **Validation Layers:** Compiles transient test keystores (`.jks`) to verify formatting logic before workspace purges.

### 6. enterprise-network-mesh
- **Core Function:** Manages cross-premises routing policies, perimeter validations, and site-to-site VPN monitoring.
- **Key Modules:** `verify_external_boundaries.yml`, `verify_vpn_tunnel.py`, `validate_cisco_context.py`.
- **Validation Layers:** Schedules automated 4-hour cron audits checking DNS mapping, TLS chains, and tunnel packet drops.
