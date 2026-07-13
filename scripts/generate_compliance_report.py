#!/usr/bin/env python3
import os
import json
from datetime import datetime

# ==============================================================================
# Script Name: generate_compliance_report.py
# Description: Simulates an enterprise-scale compliance auditing engine. Parses 
#              simulated server node metrics across hybrid landscapes (vSphere/Azure)
#              and generates an executive markdown summary report.
# ==============================================================================

def load_mock_inventory_data():
    """
    Returns a mock collection of multi-tiered enterprise infrastructure nodes.
    This simulates pulling live states from Puppet DB, Azure Graph API, and vCenter.
    """
    return [
        {"hostname": "t0-prd-tor-db2-01", "os": "SLES 15.4", "tier": "Tier 0 Database", "hosting": "vSphere", "cis_hardened": True, "patches_pending": 0, "active_certs_valid": True},
        {"hostname": "t1-prd-az-sapapp-01", "os": "SLES 15.7", "tier": "Tier 1 Application", "hosting": "Azure", "cis_hardened": True, "patches_pending": 2, "active_certs_valid": True},
        {"hostname": "t2-uat-tor-caddy-01", "os": "Ubuntu 24.04", "tier": "Tier 2 DMZ Proxy", "hosting": "vSphere", "cis_hardened": True, "patches_pending": 0, "active_certs_valid": False}, # Expiring Cert
        {"hostname": "t1-isit-tor-liberty-02", "os": "Ubuntu 22.04", "tier": "Tier 1 Application", "hosting": "vSphere", "cis_hardened": False, "patches_pending": 14, "active_certs_valid": True} # Out of compliance
    ]

def evaluate_compliance(inventory):
    """
    Analyzes raw inventory data against corporate security baselines.
    """
    total_nodes = len(inventory)
    compliant_nodes = 0
    drift_details = []

    for node in inventory:
        issues = []
        if not node["cis_hardened"]:
            issues.append("Fails CIS Benchmark baseline profile rules")
        if node["patches_pending"] > 5:
            issues.append(f"Critical patch drift detected: {node['patches_pending']} packages outstanding")
        if not node["active_certs_valid"]:
            issues.append("TLS Keystore contains an expired or expiring certificate chain")

        if len(issues) == 0:
            compliant_nodes += 1
        else:
            drift_details.append({"hostname": node["hostname"], "tier": node["tier"], "issues": issues})

    compliance_percentage = (compliant_nodes / total_nodes) * 100
    return total_nodes, compliant_nodes, compliance_percentage, drift_details

def generate_markdown_report(total, compliant, percentage, issues):
    """
    Generates a structured dashboard file detailing corporate compliance metrics.
    """
    report_path = "reports/COMPLIANCE_SUMMARY.md"
    os.makedirs("reports", exist_ok=True)

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    markdown_content = f"""# Enterprise Hybrid-Cloud Compliance Audit Report

## Execution Metadata
- **Audit Timestamp:** {current_time}
- **Target Landscape:** Institutional Hybrid Fabric (vSphere Core & Azure VNet Enclaves)
- **Compliance Baseline:** CIS Benchmarks / Enterprise Governance Policy v4.2

## Executive Dashboard Metrics

| Metric Category | System Count / Percentage | Status Indicator |
| :--- | :--- | :--- |
| **Total Tracked Assets** | {total} Nodes | Consolidated Inventory |
| **Fully Compliant Nodes** | {compliant} Nodes | Verified Stable |
| **Global Compliance Rating** | {percentage:.1f}% | {'🔴 Action Required' if percentage < 90 else '🟢 Within Acceptable Limits'} |

## Active Compliance Drift & Discrepancies
The following anomalies were flagged by the orchestration verification layer and require remediation pipelines or automated change tickets:

"""
    if not issues:
        markdown_content += "🟢 **Zero drift detected across all scanned target environments.**\n"
    else:
        for item in issues:
            markdown_content += f"### ⚠️ Node: {item['hostname']} ({item['tier']})\n"
            for issue in item['issues']:
                markdown_content += f"- [ ] {issue}\n"
            markdown_content += "\n"

    with open(report_path, "w") as report_file:
        report_file.write(markdown_content)
    
    print(f"[SUCCESS] Compliance analysis generated successfully at: {report_path}")

if __name__ == "__main__":
    raw_data = load_mock_inventory_data()
    total, compliant, pct, drift = evaluate_compliance(raw_data)
    generate_markdown_report(total, compliant, pct, drift)
