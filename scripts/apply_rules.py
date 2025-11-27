#!/usr/bin/env python3
import sys
import os

# Add parent directory to path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.firewall_manager import FirewallManager

if len(sys.argv) < 2:
    print("Usage: python3 apply_rules.py <role>")
    sys.exit(1)

role = sys.argv[1]
fw = FirewallManager()
if fw.apply_role_rules(role):
    print(f"Successfully applied rules for {role}")
else:
    print(f"Failed to apply rules for {role}")
