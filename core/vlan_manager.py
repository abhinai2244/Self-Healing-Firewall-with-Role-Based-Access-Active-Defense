import subprocess
import os
import logging

# Determine paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
DEFAULT_SCRIPT_DIR = os.path.join(BASE_DIR, 'config', 'vlan')

class VLANManager:
    def __init__(self, script_dir=DEFAULT_SCRIPT_DIR):
        self.script_dir = script_dir

    def isolate_user(self, interface):
        """
        Moves the user's interface to the isolated VLAN.
        """
        return self._run_script('vlan_isolated.sh', interface)

    def set_guest_vlan(self, interface):
        return self._run_script('vlan_guest.sh', interface)

    def set_employee_vlan(self, interface):
        return self._run_script('vlan_employee.sh', interface)

    def _run_script(self, script_name, interface):
        script_path = os.path.join(self.script_dir, script_name)
        if not os.path.exists(script_path):
            logging.error(f"Script not found: {script_path}")
            return False
        
        cmd = [script_path, interface]
        logging.info(f"Changing VLAN for {interface} using {script_name}")
        
        try:
            subprocess.run(cmd, check=True)
            logging.info(f"EXECUTED: {script_path} {interface}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to change VLAN: {e}")
            return False
