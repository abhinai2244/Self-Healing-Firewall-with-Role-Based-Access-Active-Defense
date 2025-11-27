#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rbac_manager import RBACManager

if len(sys.argv) < 2:
    print("Usage: python3 downgrade_role.py <ip_address>")
    sys.exit(1)

ip = sys.argv[1]
rbac = RBACManager()
new_role = rbac.downgrade_user(ip)

if new_role:
    print(f"User at {ip} downgraded to {new_role}")
else:
    print(f"User not found or already at lowest level")
