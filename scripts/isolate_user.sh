#!/bin/bash
# Wrapper to isolate a user interface

if [ -z "$1" ]; then
    echo "Usage: $0 <interface>"
    exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
$DIR/../config/vlan/vlan_isolated.sh $1
