#!/bin/bash
# Move interface to Employee VLAN (20)
# Usage: ./vlan_employee.sh <interface>
IFACE=$1
if [ -z "$IFACE" ]; then echo "Usage: $0 <interface>"; exit 1; fi
sudo vconfig add $IFACE 20
sudo ip link set $IFACE.20 up
echo "Moved $IFACE to VLAN 20 (Employee)"
