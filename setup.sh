#!/bin/bash

# Update package lists
sudo apt update

# Install required Linux packages
sudo apt install -y iptables iptables-persistent
sudo apt install -y snort
sudo apt install -y vlan
sudo apt install -y apache2-utils
sudo apt install -y python3-pip

# Install Python requirements
pip3 install -r requirements.txt

# Create log files if they don't exist
touch logs/firewall.log
touch logs/snort_alerts.log
touch logs/system.log

echo "Setup complete."
