import unittest
from unittest.mock import patch
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.rbac_manager import RBACManager

class TestRBAC(unittest.TestCase):
    def setUp(self):
        self.mock_roles = {
            "1.2.3.4": {"role": "admin", "username": "test"}
        }
        self.patcher = patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=json.dumps(self.mock_roles))
        self.mock_open = self.patcher.start()
        # Also patch os.path.exists to return True
        self.exists_patcher = patch('os.path.exists', return_value=True)
        self.exists_patcher.start()
        
        self.rbac = RBACManager()

    def tearDown(self):
        self.patcher.stop()
        self.exists_patcher.stop()

    def test_downgrade(self):
        with patch.object(self.rbac, 'save_roles') as mock_save:
            new_role = self.rbac.downgrade_user("1.2.3.4")
            self.assertEqual(new_role, "employee")
            self.assertEqual(self.rbac.roles_data["1.2.3.4"]["role"], "employee")
            mock_save.assert_called()

if __name__ == '__main__':
    unittest.main()
