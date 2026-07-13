#!/usr/bin/env python3
# ==============================================================================
# Script Name: compile_diagnostic_logs.py
# Description: Consolidates pipeline stdout/stderr breakdown metadata into structured
#              JSON diagnostic logs for accelerated incident triage.
# ==============================================================================

import os
import sys
import json
from datetime import datetime

def generate_diagnostic_block(pipeline_component, error_summary, trace_details):
    """
    Formulates a standardized troubleshooting schema and saves it to a 
    persistent directory path for analysis or downstream alerting integrations.
    """
    target_log_dir = "logs/diagnostics"
    os.makedirs(target_log_dir, exist_ok=True)
    
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    log_filename = f"{target_log_dir}/err_{pipeline_component}_{timestamp}.json"
    
    # Standard operational troubleshooting payload
    diagnostic_payload = {
        "metadata": {
            "component": pipeline_component,
            "error_timestamp_utc": datetime.utcnow().isoformat(),
            "infrastructure_scope": "Hybrid Boundary Mesh"
        },
        "incident_details": {
            "summary": error_summary,
            "raw_traceback_excerpt": trace_details,
            "environment_context": os.getenv("DEPLOY_ENV", "UNKNOWN-TIER")
        }
    }
    
    with open(log_filename, "w") as log_file:
        json.dump(diagnostic_payload, log_file, indent=2)
        
    print(f"[SUCCESS] Diagnostic troubleshooting package compiled at: {log_filename}")
    return log_filename

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python compile_diagnostic_logs.py <COMPONENT> <SUMMARY> <TRACE>")
        sys.exit(1)
    generate_diagnostic_block(sys.argv, sys.argv, sys.argv)
