import json
import os
import logging

# Determine paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
DEFAULT_CONFIG_PATH = os.path.join(BASE_DIR, 'config', 'rbac', 'roles.json')

class RBACManager:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.roles_data = self._load_roles()
        self.role_hierarchy = ['isolated', 'guest', 'employee', 'admin']

    def _load_roles(self):
        if not os.path.exists(self.config_path):
            return {}
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def save_roles(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.roles_data, f, indent=4)

    def get_user_by_ip(self, ip):
        return self.roles_data.get(ip)

    def update_role(self, ip, new_role):
        if ip in self.roles_data:
            old_role = self.roles_data[ip]['role']
            self.roles_data[ip]['role'] = new_role
            self.save_roles()
            logging.info(f"User {ip} role changed from {old_role} to {new_role}")
            return True
        return False

    def downgrade_user(self, ip):
        user = self.get_user_by_ip(ip)
        if not user:
            return None
        
        current_role = user['role']
        try:
            current_index = self.role_hierarchy.index(current_role)
            if current_index > 0:
                new_role = self.role_hierarchy[current_index - 1]
                self.update_role(ip, new_role)
                return new_role
        except ValueError:
            pass
        return current_role

    def isolate_user(self, ip):
        return self.update_role(ip, 'isolated')

    def restore_user(self, ip, target_role='guest'):
        # In a real scenario, we might restore to their previous role or a default safe role
        return self.update_role(ip, target_role)
