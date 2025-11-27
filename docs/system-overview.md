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
