# Self-Healing Firewall with Role-Based Access (Active Defense)

## Overview
This project implements a self-healing firewall system that uses Snort for intrusion detection and dynamically updates IPtables firewall rules based on user behavior. It features a Role-Based Access Control (RBAC) system where users can be downgraded or isolated if suspicious activity is detected.

## Project Directory Structure

```
self-healing-firewall/
│
├── docs/
│   ├── architecture-diagram.png
│   ├── rbac-flow.pdf
│   └── system-overview.md
│
├── config/
│   ├── iptables/
│   │   ├── base_rules.v4
│   │   ├── guest_rules.v4
│   │   ├── employee_rules.v4
│   │   └── admin_rules.v4
│   │
│   ├── snort/
│   │   ├── snort.conf
│   │   ├── rules/
│   │   │   └── local.rules
│   │   └── classification.config
│   │
│   ├── rbac/
│   │   └── roles.json
│   │
│   ├── vlan/
│   │   ├── vlan_guest.sh
│   │   ├── vlan_isolated.sh
│   │   └── vlan_employee.sh
│   │
│   └── system.conf
│
├── scripts/
│   ├── apply_rules.py
│   ├── downgrade_role.py
│   ├── parse_snort_logs.py
│   ├── isolate_user.sh
│   ├── restore_role.py
│   └── startup.sh
│
├── core/
│   ├── firewall_manager.py
│   ├── rbac_manager.py
│   ├── snort_monitor.py
│   ├── vlan_manager.py
│   └── event_engine.py
│
├── web_dashboard/
│   ├── app.py
│   ├── templates/
│   │   ├── index.html
│   │   ├── logs.html
│   │   └── bans.html
│   └── static/
│       ├── css/
│       └── js/
│
├── logs/
│   ├── firewall.log
│   ├── snort_alerts.log
│   └── system.log
│
├── tests/
│   ├── test_firewall.py
│   ├── test_rbac.py
│   └── test_snort.py
│
├── requirements.txt
├── README.md
└── setup.sh
```

## Setup
1. Run `./setup.sh` to install dependencies (requires sudo).
2. Configure roles in `config/rbac/roles.json`.
3. Start the system using `scripts/startup.sh`.

## Dashboard
Access the dashboard at `http://localhost:5000`.
Default credentials should be configured in the app.

## Architecture
- **Snort** detects anomalies.
- **Event Engine** processes alerts.
- **RBAC Manager** downgrades user roles.
- **Firewall Manager** updates rules.
- **VLAN Manager** isolates users.
