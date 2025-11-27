import time
import logging
import threading
import re
import os
import sys

# Ensure we can import sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rbac_manager import RBACManager
from core.firewall_manager import FirewallManager
from core.vlan_manager import VLANManager

# Determine paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
LOG_DIR = os.path.join(BASE_DIR, 'logs')
SYSTEM_LOG = os.path.join(LOG_DIR, 'system.log')
SNORT_LOG = os.path.join(LOG_DIR, 'snort_alerts.log')

# Create logs directory if it doesn't exist (for safety)
if not os.path.exists(LOG_DIR):
    try:
        os.makedirs(LOG_DIR)
    except OSError:
        pass # Might be permissions or exist

# Setup Logging
logging.basicConfig(
    filename=SYSTEM_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class EventEngine:
    def __init__(self):
        self.rbac = RBACManager()
        self.firewall = FirewallManager()
        self.vlan = VLANManager()
        self.cooldown_tracker = {} # IP -> timestamp
        self.cooldown_period = 300 # 5 minutes

    def process_snort_alert(self, log_line):
        """
        Parses a Snort log line and triggers actions.
        Example line: [**] [1:1000001:0] Malware Download [**] [Priority: 1] {TCP} 192.168.1.10:1234 -> 1.2.3.4:80
        """
        logging.info(f"Processing Alert: {log_line.strip()}")
        
        # Regex to extract IP (simplified)
        # Looking for Source IP. Assuming internal IPs are 192.168.x.x
        match = re.search(r'\{TCP\} (\d+\.\d+\.\d+\.\d+)', log_line)
        if not match:
            # Try UDP or just looking for IP pattern
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', log_line)
        
        if match:
            source_ip = match.group(1)
            self.handle_threat(source_ip, log_line)

    def handle_threat(self, ip, reason):
        logging.warning(f"Threat detected from {ip}. Action: Downgrade/Isolate")
        
        user = self.rbac.get_user_by_ip(ip)
        if not user:
            logging.warning(f"Unknown IP {ip}, blocking directly.")
            self.firewall.block_ip(ip)
            return

        # Downgrade Role
        new_role = self.rbac.downgrade_user(ip)
        logging.info(f"User {user['username']} downgraded to {new_role}")
        
        # Apply new firewall rules
        # In a real per-user system, we'd apply specific rules for this user.
        # Here we demonstrate the concept.
        self.firewall.apply_role_rules(new_role)

        # If isolated, switch VLAN
        if new_role == 'isolated':
            # Assuming we can map IP to Interface (e.g., via a lookup or just 'eth0' for demo)
            # In a real world, this needs complex mapping
            interface = "eth0" # Placeholder
            self.vlan.isolate_user(interface)

        # Record for cooldown
        self.cooldown_tracker[ip] = time.time()

    def check_cooldowns(self):
        """
        Periodically checks if users can be restored.
        """
        now = time.time()
        to_remove = []
        for ip, timestamp in self.cooldown_tracker.items():
            if now - timestamp > self.cooldown_period:
                logging.info(f"Cooldown expired for {ip}. Restoring role.")
                self.rbac.restore_user(ip, 'guest') # Restore to safe baseline
                self.firewall.apply_role_rules('guest')
                to_remove.append(ip)
        
        for ip in to_remove:
            del self.cooldown_tracker[ip]

    def run_loop(self):
        while True:
            self.check_cooldowns()
            time.sleep(10)

if __name__ == "__main__":
    from core.snort_monitor import SnortMonitor
    
    engine = EventEngine()
    
    # Start Snort Monitor
    # Use the calculated path
    monitor = SnortMonitor(SNORT_LOG, engine.process_snort_alert)
    monitor.start()
    
    try:
        logging.info("Event Engine Started")
        engine.run_loop()
    except KeyboardInterrupt:
        monitor.stop()
        logging.info("Event Engine Stopped")
