import os
import subprocess
import logging
import sys

# Try to import python-iptables, but fallback if not available (for demo/sandbox)
try:
    import iptc
    HAS_IPTC = True
except (ImportError, PermissionError):
    HAS_IPTC = False

# Determine paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
DEFAULT_CONFIG_DIR = os.path.join(BASE_DIR, 'config', 'iptables')

class FirewallManager:
    def __init__(self, config_dir=DEFAULT_CONFIG_DIR):
        self.config_dir = config_dir

    def apply_role_rules(self, role):
        """
        Applies the iptables rules file corresponding to the role.
        """
        rule_file = os.path.join(self.config_dir, f"{role}_rules.v4")
        if not os.path.exists(rule_file):
            logging.error(f"Rule file for role {role} not found: {rule_file}")
            return False

        logging.info(f"Applying firewall rules for role: {role} from {rule_file}")
        
        if HAS_IPTC:
            # Demonstration of using python-iptables logic
            try:
                # In a real scenario we would flush and reload chains
                pass
            except Exception as e:
                logging.warning(f"Failed to use python-iptables: {e}")

        try:
            # Execute iptables-restore
            # In production we want this to run. In tests it will be mocked.
            # We use shell=True to allow redirection <
            subprocess.run(f"iptables-restore < {rule_file}", shell=True, check=True)
            logging.info(f"EXECUTED: iptables-restore < {rule_file}")
            return True
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to apply rules: {e}")
            return False

    def block_ip(self, ip):
        """
        Explicitly blocks an IP using iptables.
        """
        logging.info(f"Blocking IP: {ip}")
        if HAS_IPTC:
            try:
                chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
                rule = iptc.Rule()
                rule.src = ip
                rule.target = iptc.Target(rule, "DROP")
                chain.insert_rule(rule)
                return True
            except Exception as e:
                logging.warning(f"Could not use iptc to block: {e}")
        
        # Fallback to subprocess
        cmd = f"iptables -A INPUT -s {ip} -j DROP"
        try:
            subprocess.run(cmd, shell=True, check=True)
            logging.info(f"EXECUTED: {cmd}")
            return True
        except subprocess.CalledProcessError as e:
             logging.error(f"Failed to block IP: {e}")
             return False
