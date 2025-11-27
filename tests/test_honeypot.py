import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import threading
import socket
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.honeypot import start_honeypot, HONEYPOT_PORT

class TestHoneypot(unittest.TestCase):
    def test_honeypot_connection(self):
        # We can't easily test the loop, but we can test if the port opens if we run it in a thread
        # However, CI/CD environments might block binding ports.
        # We will mock socket to ensure logic is correct.
        
        with patch('socket.socket') as mock_socket:
            mock_srv = MagicMock()
            mock_socket.return_value = mock_srv
            
            # Simulate one accept then raise exception to break loop
            mock_client = MagicMock()
            mock_srv.accept.side_effect = [(mock_client, ('1.2.3.4', 5555)), Exception("Break Loop")]
            
            try:
                start_honeypot()
            except Exception:
                pass
            
            # Check if accept was called
            mock_srv.accept.assert_called()
            # Check if it tried to write to file (we didn't mock open, so it might fail or write to real file)
            # To be safe, we should mock open too.

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('socket.socket')
    def test_honeypot_logging(self, mock_socket, mock_open):
        mock_srv = MagicMock()
        mock_socket.return_value = mock_srv
        mock_client = MagicMock()
        # Return client, then break loop
        mock_srv.accept.side_effect = [(mock_client, ('1.2.3.4', 5555)), Exception("Break")]
        
        try:
            start_honeypot()
        except Exception:
            pass
            
        # Check if it wrote to the log file
        mock_open.assert_called()
        handle = mock_open()
        # Verify write content contains HONEYPOT TRIGGERED
        handle.write.assert_called()
        args, _ = handle.write.call_args
        self.assertIn("HONEYPOT TRIGGERED", args[0])

if __name__ == '__main__':
    unittest.main()
