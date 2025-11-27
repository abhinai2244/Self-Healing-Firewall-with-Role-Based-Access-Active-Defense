#!/bin/bash
# Move interface to Guest VLAN (10)
# Usage: ./vlan_guest.sh <interface>
IFACE=$1
if [ -z "$IFACE" ]; then echo "Usage: $0 <interface>"; exit 1; fi
sudo vconfig add $IFACE 10
sudo ip link set $IFACE.10 up
echo "Moved $IFACE to VLAN 10 (Guest)"
