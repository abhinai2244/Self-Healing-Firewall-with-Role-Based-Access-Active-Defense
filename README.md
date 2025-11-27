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


# System Overview

## Introduction
The Self-Healing Firewall with Role-Based Access (Active Defense) is designed to automatically detect malicious activity within a network and mitigate threats by dynamically adjusting user privileges and network access rules.

## High-Level Architecture

The system consists of the following components:

1.  **Snort (Intrusion Detection System)**: Monitors network traffic in real-time and logs suspicious activities based on predefined rules.
2.  **Event Engine**: The core logic that consumes Snort logs, analyzes threats, and triggers mitigation actions.
3.  **RBAC Manager**: Manages user roles (Admin, Employee, Guest, Isolated) and handles role transitions (downgrades/restorations).
4.  **Firewall Manager**: Applies iptables rules corresponding to the user's current role.
5.  **VLAN Manager**: Moves user interfaces to different VLANs for isolation purposes.
6.  **Web Dashboard**: Provides a visual interface for administrators to monitor logs, view active bans, and manually manage roles.

## Workflow

1.  **Detection**: Snort detects a signature match (e.g., malware download) and writes to `snort_alerts.log`.
2.  **Ingestion**: The `SnortMonitor` (part of Event Engine) detects the new log entry.
3.  **Processing**: The `EventEngine` parses the log to identify the source IP.
4.  **Mitigation**:
    *   The user associated with the IP is identified via `roles.json`.
    *   The `RBACManager` downgrades the user's role (e.g., Admin -> Employee).
    *   The `FirewallManager` applies the new rule set for that role.
    *   If the user reaches "Isolated" status, the `VLANManager` moves them to the isolation VLAN.
5.  **Recovery**: After a cooldown period (default 5 minutes), the system automatically restores the user to a baseline role (Guest).

## Security Considerations

-   **Fail-Safe**: In case of errors, the system logs the issue but aims to keep the network operational.
-   **Authentication**: The dashboard is protected by password authentication.
-   **Logging**: All actions are logged to `system.log` for audit trails.


