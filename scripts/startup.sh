#!/bin/bash
echo "Starting Self-Healing Firewall System..."

# Ensure permissions
chmod +x ../config/vlan/*.sh
chmod +x *.sh

# Start Event Engine in background
nohup python3 ../core/event_engine.py > ../logs/system.log 2>&1 &
echo "Event Engine started (PID: $!)"

# Start Web Dashboard
nohup python3 ../web_dashboard/app.py > ../logs/dashboard.log 2>&1 &
echo "Web Dashboard started (PID: $!)"

echo "System is running."
