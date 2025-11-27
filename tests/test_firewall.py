import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.firewall_manager import FirewallManager

class TestFirewall(unittest.TestCase):
    @patch('subprocess.run')
    @patch('core.firewall_manager.HAS_IPTC', False) 
    def test_apply_rules(self, mock_subprocess):
        fw = FirewallManager()
        # Mock os.path.exists to True
        with patch('os.path.exists', return_value=True):
            success = fw.apply_role_rules("guest")
            self.assertTrue(success)
            mock_subprocess.assert_called()

if __name__ == '__main__':
    unittest.main()
