#!/usr/bin/env python3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rbac_manager import RBACManager

if len(sys.argv) < 3:
    print("Usage: python3 restore_role.py <ip> <role>")
    sys.exit(1)

ip = sys.argv[1]
role = sys.argv[2]
rbac = RBACManager()

if rbac.update_role(ip, role):
    print(f"User {ip} restored to {role}")
else:
    print("Failed to restore user.")
