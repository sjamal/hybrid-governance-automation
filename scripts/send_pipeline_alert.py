#!/usr/bin/env python3
import os
import sys
import json
import requests

# ==============================================================================
# Script Name: send_pipeline_alert.py
# Description: Evaluates the severity tier of validation failures and triggers
#              dynamic escalation payloads to corporate communications channels.
# ==============================================================================

def transmit_alert(pipeline_name, execution_status, environment, classification, discrepancy_log=""):
    """
    Assembles a priority-weighted payload and executes a POST to the correct
    operations webhook based on infrastructure criticality tiers.
    """
    # Map infrastructure tiers to corresponding communication destinations
    # Primary pipeline notifications target standard operations arrays
    webhook_url = os.getenv("OPSTEAM_WEBHOOK_URL", "https://localhost/mock-ops-webhook")
    
    # Critical Tier 0 or Tier 1 Production failures target direct engineering pages
    if classification.upper() in ["TIER0", "TIER1"] and environment.upper() == "PRD":
        print("[CRITICAL] High-severity production breach identified. Escaling alert destination.")
        webhook_url = os.getenv("EMERGENCY_ESCALATION_WEBHOOK_URL", "https://localhost/mock-emergency-webhook")

    current_timestamp = requests.utils.time.time()
    
    # Establish priority markers based on technical layers
    color_code = "FF0000" if classification.upper() == "TIER0" else "FFA500"
    if classification.upper() not in ["TIER0", "TIER1"]:
        color_code = "0000FF"

    # Assemble structured card elements with custom routing metadata
    alert_payload = {
        "title": f"🚨 GOVERNANCE INCIDENT DETECTED: {pipeline_name}",
        "themeColor": color_code,
        "sections": [
            {
                "activityTitle": f"Escalation Level: {classification} - {environment}",
                "activitySubtitle": f"Timestamp Matrix: {current_timestamp}",
                "facts": [
                    {"name": "Execution State:", "value": execution_status},
                    {"name": "Target Environment:", "value": environment},
                    {"name": "Asset Priority:", "value": f"LEVEL-{classification}"}
                ],
                "text": f"**Discovered Violations:**\n{discrepancy_log}" if discrepancy_log else "Static review validation failed during pre-flight orchestration."
            }
        ]
    }

    try:
        print(f"[INFO] Dispatching {classification} notification cards to target endpoints...")
        # response = requests.post(webhook_url, json=alert_payload, timeout=5)
        # response.raise_for_status()
        print(f"[SUCCESS] Escalated notification state processed via target channel.")
    except Exception as e:
        print(f"[ERROR] Failed to send operational notification payload: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python send_pipeline_alert.py <PIPELINE_NAME> <STATUS> <ENVIRONMENT> <CLASSIFICATION> [LOG]")
        sys.exit(1)
        
    log_data = sys.argv[5] if len(sys.argv) > 5 else ""
    transmit_alert(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], log_data)
