#!/usr/bin/env python3
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python3 parse_snort_logs.py <log_file>")
    sys.exit(1)

log_file = sys.argv[1]

try:
    with open(log_file, 'r') as f:
        for line in f:
            if "[**]" in line:
                print(line.strip())
except FileNotFoundError:
    print("Log file not found.")
