# Architectural Decision Record 0008: S2S VPN Monitoring and Scheduled Audits

## Context & Operational Challenges
Infrastructure boundaries can degrade due to configuration drifts, routing parameter flushes, or key renegotiation errors on crypto engines. Relying strictly on event-driven (commit-based) pipeline execution means perimeter cracks or transit blackouts might remain unnoticed until a user deployment fails.

## Decision Parameters
The infrastructure architecture will adopt a scheduled cron execution layer within the Azure DevOps Pipeline engine. 

This tracking framework runs independently of development loops, executing network path transit pings via Python across the Site-to-Site (S2S) VPN tunnel, while simultaneously running automated multi-layer ingress audits via Ansible playbooks against AppGW and APIM perimeters.

## System Performance Outcomes
- **Continuous Health Visibility:** Transitions boundary verification from a reactive deployment checkpoint into an automated, proactive monitoring daemon.
- **Isolated Testing Domains:** Decouples perimeter performance analysis tools from runtime application code delivery engines.
- **Fast Transit Detection:** Captures packet loss or route drops over internal hybrid tunnels before configurations are pushed out to environments.
