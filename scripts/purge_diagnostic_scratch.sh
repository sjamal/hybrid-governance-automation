#!/bin/bash
# ==============================================================================
# Script Name: purge_diagnostic_scratch.sh
# Description: Flushes temporary validation artifacts, JSON crash traces, and
#              diagnostic files from build nodes after alerting cycles finish.
# ==============================================================================

set -euo pipefail

# Define the target diagnostic logging directories
DIAGNOSTIC_DIR="./logs/diagnostics"

echo "[INFO] Commencing post-alert workflow workspace remediation..."

if [ -d "${DIAGNOSTIC_DIR}" ]; then
    echo "[INFO] Auditing scratch zone storage sizes before deletion..."
    # Record dynamic metadata logs to track environment sizing properties
    file_count=$(find "${DIAGNOSTIC_DIR}" -type f -name "*.json" | wc -l)
    echo "[INFO] Discovered ${file_count} temporary structural execution trace files to purge."
    
    # Safely clear the tracking folders to protect runner node space boundaries
    find "${DIAGNOSTIC_DIR}" -type f -name "err_*.json" -exec rm -f {} +
    echo "[SUCCESS] Ephemeral diagnostic JSON logs purged safely."
else
    echo "[INFO] No temporary diagnostic scratch zones identified. Cleanup step omitted."
fi

exit 0
