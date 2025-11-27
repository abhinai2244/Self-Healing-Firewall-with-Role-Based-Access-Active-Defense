import socket
import logging
import time
import os
import sys

# Configure where to write alerts
# We write to the same log file that Snort uses, so the Event Engine picks it up automatically.
BASE_DIR = os.path.dirname(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
SNORT_LOG = os.path.join(BASE_DIR, 'logs', 'snort_alerts.log')
HONEYPOT_PORT = 2323

def start_honeypot():
    # Create socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind(('0.0.0.0', HONEYPOT_PORT))
        server_socket.listen(5)
        print(f"[*] Honeypot listening on port {HONEYPOT_PORT}...")
    except PermissionError:
        print(f"[!] Permission denied binding to port {HONEYPOT_PORT}. Try using a port > 1024.")
        return

    while True:
        try:
            client_socket, addr = server_socket.accept()
            ip = addr[0]
            port = addr[1]
            print(f"[!] Honeypot trigger from {ip}:{port}")
            
            # Log the alert in Snort format so EventEngine picks it up
            # Format: [**] [SID] Message [**] {Proto} SourceIP -> DestIP
            log_entry = f"[**] [1:999999:1] HONEYPOT TRIGGERED [**] [Priority: 1] {{TCP}} {ip}:{port} -> 127.0.0.1:{HONEYPOT_PORT}\n"
            
            with open(SNORT_LOG, 'a') as f:
                f.write(log_entry)
            
            client_socket.close()
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    start_honeypot()
