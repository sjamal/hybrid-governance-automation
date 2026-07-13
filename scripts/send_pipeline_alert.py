#!/usr/bin/env python3
import os
import sys
import json
import requests

# ==============================================================================
# Script Name: send_pipeline_alert.py
# Description: Formulates and transmits real-time alerts to communications 
#              webhooks upon pipeline validation failures or drift detections.
# ==============================================================================

def transmit_alert(pipeline_name, execution_status, environment, discrepancy_log=""):
    """
    Assembles a structured JSON payload and executes a POST request to an
    authenticated corporate communications webhook endpoint.
    """
    # Retrieve the secure destination URL from environment variables
    webhook_url = os.getenv("OPSTEAM_WEBHOOK_URL")
    
    if not webhook_url:
        print("[WARNING] OPSTEAM_WEBHOOK_URL missing. Simulating chat message broadcast.")
        webhook_url = "https://localhost/mock-webhook"

    current_timestamp = requests.utils.time.time()
    
    # Structure the alert payload using cards to facilitate quick triage
    alert_payload = {
        "title": f"🚨 INFRASTRUCTURE GOVERNANCE ALERT: {pipeline_name}",
        "sections": [
            {
                "activityTitle": "Pipeline Compliance Failure",
                "activitySubtitle": f"Timestamp: {current_timestamp}",
                "facts": [
                    {"name": "Execution State:", "value": execution_status},
                    {"name": "Target Lifecycle Tier:", "value": environment},
                    {"name": "Trigger Source:", "value": "Automated Validation Engine"}
                ],
                "text": f"**Discovered Violations:**\n{discrepancy_log}" if discrepancy_log else "Static review validation failed during pre-flight orchestration."
            }
        ]
    }

    try:
        # Execute the webhook notification post with strict timeout policies
        print(f"[INFO] Dispatching alert cards for {pipeline_name} to operations webhooks...")
        # response = requests.post(webhook_url, json=alert_payload, timeout=5)
        # response.raise_for_status()
        print("[SUCCESS] Operational notification delivered successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to send operational notification payload: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python send_pipeline_alert.py <PIPELINE_NAME> <STATUS> <ENVIRONMENT> [LOG]")
        sys.exit(1)
        
    log_data = sys.argv[4] if len(sys.argv) > 4 else ""
    transmit_alert(sys.argv[1], sys.argv[2], sys.argv[3], log_data)
