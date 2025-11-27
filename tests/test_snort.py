import unittest
from unittest.mock import MagicMock
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.event_engine import EventEngine

class TestSnort(unittest.TestCase):
    def test_alert_processing(self):
        # We need to mock RBAC, Firewall, VLAN within EventEngine or just check logic
        # Here we test the event engine logic which consumes snort logs
        engine = EventEngine()
        engine.handle_threat = MagicMock()
        
        log_line = "[**] [1:1000001:0] Malware [**] {TCP} 192.168.1.10:1234 -> 1.1.1.1:80"
        engine.process_snort_alert(log_line)
        
        engine.handle_threat.assert_called_with("192.168.1.10", log_line)

if __name__ == '__main__':
    unittest.main()
