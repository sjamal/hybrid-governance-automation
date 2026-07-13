import os
import sys
import requests

def check_servicenow_change_window(change_id, environment):
    """
    Simulates a production guardrail check against the ServiceNow API.
    Ensures that a change ticket is Approved and within its active window
    before Jenkins or Azure DevOps triggers configurations in PRD/UAT.
    """
    # In production, these are securely fetched from Azure Key Vault or Jenkins Secrets
    SNOW_USER = os.getenv("SNOW_USER", "mock_api_user")
    SNOW_PASS = os.getenv("SNOW_PASS", "mock_secure_password")
    SNOW_URL = f"https://service-now.com{change_id}"

    # Environments that require strict change control
    if environment.upper() in ["PRD", "UAT"]:
        print(f"[INFO] Evaluating change governance for {change_id} on {environment}...")
        try:
            # Mocking the request execution for open-source safety
            # response = requests.get(SNOW_URL, auth=(SNOW_USER, SNOW_PASS), timeout=10)
            # data = response.json()
            
            # Simulated Payload Response
            mock_state = "Approved" 
            
            if mock_state != "Approved":
                print(f"[CRITICAL] Change {change_id} is in status '{mock_state}'. Aborting deployment.")
                sys.exit(1)
                
            print(f"[SUCCESS] Change {change_id} is APPROVED. Proceeding with infrastructure tasks.")
            
        except Exception as e:
            print(f"[ERROR] Failed to verify ServiceNow governance: {str(e)}")
            sys.exit(1)
    else:
        print(f"[INFO] Environment {environment} does not require a ServiceNow change ticket. Proceeding.")

if __name__ == "__main__":
    # Example execution via pipeline: python servicenow_change_gate.py CHG0019283 PRD
    if len(sys.argv) < 3:
        print("Usage: python servicenow_change_gate.py <CHANGE_ID> <ENVIRONMENT>")
        sys.exit(1)
    check_servicenow_change_window(sys.argv[1], sys.argv[2])

