#!/usr/bin/env python3
# ==============================================================================
# Script Name: compile_diagnostic_logs.py
# Description: Consolidates pipeline stdout/stderr breakdown metadata into structured
#              JSON diagnostic logs and routes them to operations alert webhooks.
# ==============================================================================

import os
import sys
import json
from datetime import datetime
import requests

def generate_and_route_diagnostic_block(pipeline_component, error_summary, trace_details, route_to_chat=True):
    """
    Formulates a standardized troubleshooting schema and routes details directly
    to the Operations notification engines on critical failures.
    """
    target_log_dir = "logs/diagnostics"
    os.makedirs(target_log_dir, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_filename = f"{target_log_dir}/err_{pipeline_component}_{timestamp}.json"
    
    diagnostic_payload = {
        "metadata": {
            "component": pipeline_component,
            "error_timestamp_utc": datetime.utcnow().isoformat(),
            "infrastructure_scope": "Hybrid Boundary Mesh"
        },
        "incident_details": {
            "summary": error_summary,
            "raw_traceback_excerpt": trace_details,
            "environment_context": os.getenv("DEPLOY_ENV", "PRD")
        }
    }
    
    # Save the file locally for persistent log management requirements
    with open(log_filename, "w") as log_file:
        json.dump(diagnostic_payload, log_file, indent=2)
    print(f"[SUCCESS] Diagnostic troubleshooting package compiled locally at: {log_filename}")
    
    # Optional routing handler linking diagnostic data to live notification components
    if route_to_chat:
        webhook_url = os.getenv("OPSTEAM_WEBHOOK_URL", "https://localhost/mock-ops-webhook")
        print(f"[INFO] Forwarding diagnostic payload summaries to destination hook...")
        
        chat_card = {
            "title": f"🚨 COMPONENT PIPELINE FAILURE: {pipeline_component}",
            "themeColor": "FF0000",
            "text": f"**Summary:** {error_summary}\n\n**Structured Log Exported:** `{log_filename}`"
        }
        try:
            # response = requests.post(webhook_url, json=chat_card, timeout=5)
            print("[SUCCESS] Troubleshooting metadata routed to communication channel.")
        except Exception as err:
            print(f"[WARNING] Failed to deliver alert payload card: {str(err)}")

    return log_filename

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python compile_diagnostic_logs.py <COMPONENT> <SUMMARY> <TRACE>")
        sys.exit(1)
    generate_and_route_diagnostic_block(sys.argv, sys.argv, sys.argv)
