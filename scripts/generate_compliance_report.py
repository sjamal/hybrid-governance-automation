#!/usr/bin/env python3
import os
import json
from datetime import datetime

# ==============================================================================
# Script Name: generate_compliance_report.py
# Description: Evaluates multi-cloud and on-premises infrastructure inventories 
#              against corporate safety metrics. Captures layout data including 
#              regional tags, availability zones, and security perimeters.
# ==============================================================================

def load_mock_inventory_data():
    """
    Returns a unified infrastructure matrix spanning Azure and vSphere environments.
    Simulates real data parsed from cloud resource graphs and local asset databases.
    """
    return [
        {
            "hostname": "prd-cae-sapapp-01", 
            "os": "SLES 15.7", 
            "network_zone": "Tier 0 SAP Core", 
            "platform": "Azure", 
            "region": "canadaeast", 
            "availability_zone": "CA East AZ-1", 
            "cis_hardened": True, 
            "patches_pending": 0, 
            "active_certs_valid": True,
            "classification": "Tier0"
        },
        {
            "hostname": "prd-caw-sapdb-01", 
            "os": "SLES 15.7", 
            "network_zone": "Tier 0 SAP DB", 
            "platform": "Azure", 
            "region": "canadacentral", 
            "availability_zone": "CA Central AZ-2", 
            "cis_hardened": True, 
            "patches_pending": 1, 
            "active_certs_valid": True,
            "classification": "Tier0"
        },
        {
            "hostname": "t2-uat-tor-caddy-01", 
            "os": "Ubuntu 24.04", 
            "network_zone": "Tier 2 DMZ Proxy", 
            "platform": "vSphere", 
            "region": "tor-dc-alpha", 
            "availability_zone": "ESXi-Cluster-02", 
            "cis_hardened": True, 
            "patches_pending": 0, 
            "active_certs_valid": False, # Expiring Cert
            "classification": "Tier2"
        },
        {
            "hostname": "t1-isit-tor-liberty-02", 
            "os": "Ubuntu 22.04", 
            "network_zone": "Tier 1 Application", 
            "platform": "vSphere", 
            "region": "tor-dc-beta", 
            "availability_zone": "ESXi-Cluster-01", 
            "cis_hardened": False, # Non-hardened
            "patches_pending": 14, # Patch drift
            "active_certs_valid": True,
            "classification": "Tier1"
        }
    ]

def evaluate_compliance(inventory):
    """
    Evaluates each infrastructure record against structural guardrails.
    """
    total_nodes = len(inventory)
    compliant_nodes = 0
    drift_details = []

    for node in inventory:
        issues = []
        # Enforce CIS Benchmark checks
        if not node["cis_hardened"]:
            issues.append("Fails configuration baseline checklist rules")
        # Monitor systemic patching gaps
        if node["patches_pending"] > 5:
            issues.append(f"Patch distribution variance: {node['patches_pending']} outstanding updates")
        # Track expiration timelines on certificates
        if not node["active_certs_valid"]:
            issues.append("Target service keystore reports validation failures / expired signatures")

        if len(issues) == 0:
            compliant_nodes += 1
        else:
            drift_details.append({
                "hostname": node["hostname"], 
                "network_zone": node["network_zone"], 
                "platform": node["platform"],
                "location": f"{node['region']} / {node['availability_zone']}",
                "classification": node["classification"],
                "issues": issues
            })

    compliance_percentage = (compliant_nodes / total_nodes) * 100
    return total_nodes, compliant_nodes, compliance_percentage, drift_details

def generate_markdown_report(total, compliant, percentage, issues):
    """
    Outputs a consolidated enterprise infrastructure audit dashboard.
    """
    report_path = "reports/COMPLIANCE_SUMMARY.md"
    os.makedirs("reports", exist_ok=True)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    markdown_content = f"""# Enterprise Compliance Audit Summary

## Audit Execution Context
- **Report Generation Time:** {current_time}
- **Asset Control Landscape:** Hybrid Infrastructure Footprint (Azure Subscriptions & vSphere Hosts)
- **Target Parameters:** CIS Hardening Specifications, Lifecycle Patching, Cryptographic Integrity

## High-Level Status Dashboard

| Metric Segment | Quantity / Operational State | Evaluation Status |
| :--- | :--- | :--- |
| **Tracked Infrastructure Nodes** | {total} Evaluated Assets | Monitored Platform Assets |
| **Verified Compliant Nodes** | {compliant} Validated Stables | Stable Production Integrity |
| **Systemic Compliance Rating** | {percentage:.1f}% | {'🔴 Action Required - Beyond Bounds' if percentage < 90 else '🟢 Within Acceptable Limits'} |

## Active Compliance Drift & Infrastructure Discrepancies
The platform orchestration engine discovered the following variance vectors requiring immediate remediation or lifecycle management workflows:

"""
    if not issues:
        markdown_content += "🟢 **Zero structural compliance drift identified across tracked inventory zones.**\n"
    else:
        for item in issues:
            markdown_content += f"### ⚠️ Asset: {item['hostname']} [{item['classification']}]\n"
            markdown_content += f"- **Infrastructure Layer:** {item['platform']} Cloud Topology\n"
            markdown_content += f"- **Regional / Zone Mapping:** `{item['location']}`\n"
            markdown_content += f"- **Network Boundary:** Layer-Zoned `{item['network_zone']}` Subnet Mesh\n"
            markdown_content += f"- **Discovered Drift Deviations:**\n"
            for issue in item['issues']:
                markdown_content += f"  - [ ] {issue}\n"
            markdown_content += "\n"

    with open(report_path, "w") as report_file:
        report_file.write(markdown_content)
    print(f"[SUCCESS] Enterprise compliance data published safely to: {report_path}")

if __name__ == "__main__":
    raw_data = load_mock_inventory_data()
    total, compliant, pct, drift = evaluate_compliance(raw_data)
    generate_markdown_report(total, compliant, pct, drift)
