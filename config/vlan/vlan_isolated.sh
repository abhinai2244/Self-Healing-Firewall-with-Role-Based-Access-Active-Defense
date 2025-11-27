#!/bin/bash
# Move interface to Isolated VLAN (999)
# Usage: ./vlan_isolated.sh <interface>
IFACE=$1
if [ -z "$IFACE" ]; then echo "Usage: $0 <interface>"; exit 1; fi
sudo vconfig add $IFACE 999
sudo ip link set $IFACE.999 up
echo "Moved $IFACE to VLAN 999 (Isolated)"
