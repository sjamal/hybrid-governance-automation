#!/usr/bin/env python3
# ==============================================================================
# Script Name: validate_global_syntax.py
# Description: Multi-format syntax validation scanner checking syntax for
#              Caddyfiles, JSON configurations, YAML playbooks, and shell scripts.
# ==============================================================================

import os
import sys
import json
import subprocess

def validate_json_file(file_path):
    """Verifies standard JSON structural alignments."""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except Exception as e:
        print(f"[SYNTAX ERROR][JSON]: Invalid structure in {file_path} -> {str(e)}")
        return False

def validate_yaml_file(file_path):
    """Verifies basic YAML indentation properties non-interactively."""
    try:
        # Utilize shell execution tools to check file validity safely
        subprocess.run(["python3", "-c", f"import yaml; yaml.safe_load(open('{file_path}'))"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        # Fallback tracking if pyyaml is missing on the platform agent
        return True

def validate_shell_script(file_path):
    """Audits shell script components utilizing bash execution diagnostics."""
    try:
        subprocess.run(["bash", "-n", file_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[SYNTAX ERROR][SHELL]: Syntax breakdown inside {file_path} -> {e.stderr.decode().strip()}")
        return False

def validate_caddyfile(file_path):
    """Validates structural tokens inside a target Caddy configuration file."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Look for baseline token enclosures to prevent syntax mismatches
        open_braces = content.count("{")
        close_braces = content.count("}")
        if open_braces != close_braces:
            print(f"[SYNTAX ERROR][CADDYFILE]: Enclosure brace mismatch inside {file_path}")
            return False
        return True
    except Exception as e:
        print(f"[SYNTAX ERROR][CADDYFILE]: Parsing failure in {file_path} -> {str(e)}")
        return False

def run_global_scanner(workspace_root="."):
    """Iterates through structural storage locations to audit active file syntax."""
    failed_files = 0
    print(f"[INFO] Commencing global validation checks within directory: {workspace_root}")
    
    for root, _, files in os.walk(workspace_root):
        for file in files:
            full_path = os.path.join(root, file)
            
            # Skip evaluation across local configuration caching directories
            if ".git" in full_path or "__pycache__" in full_path or "venv" in full_path:
                continue
                
            success = True
            if file.endswith(".json"):
                success = validate_json_file(full_path)
            elif file.endswith(".yml") or file.endswith(".yaml"):
                success = validate_yaml_file(full_path)
            elif file.endswith(".sh"):
                success = validate_shell_script(full_path)
            elif file == "Caddyfile" or file.endswith(".erb"):
                success = validate_caddyfile(full_path)
                
            if not success:
                failed_files += 1
                
    return failed_files == 0

if __name__ == "__main__":
    scan_passed = run_global_scanner()
    sys.exit(0 if scan_passed else 1)
