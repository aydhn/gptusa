# Incident Runbook

## Response Protocol
When an incident is detected or suspected, the operator should follow this sequence:
1. `python -m usa_signal_bot operational-health` (Check overall system status)
2. `python -m usa_signal_bot incident-review --write` (Collect artifacts and generate an incident report)
3. `python -m usa_signal_bot incident-latest` (Read the summarized report)
4. `python -m usa_signal_bot recovery-plan --latest-incident --write` (Generate a recovery plan)
5. `python -m usa_signal_bot recovery-dry-run --latest-plan` (See what actions the system suggests)
6. `python -m usa_signal_bot backup-create` (Always backup the current state before taking manual action)
7. `python -m usa_signal_bot rollback-precheck --latest-source` (If a rollback is needed, verify the source is safe)
8. `python -m usa_signal_bot rollback-dry-run --latest-plan` (Verify which files would change)
9. Perform manual review and manually execute required commands.

## Common Incident Types
- **Disk Quota Incident:** Verify disk space. Run `cleanup-dry-run`. If safe, execute cleanup manually.
- **Config Incident:** Run `validate-config` and correct typos in `.yaml`.
- **Regression Failure:** Review `regression-info`. The latest code modifications may have broken deterministic golden fixtures.
- **Safety Violation:** A protected path was targeted for modification or a secret leak was detected. Automated tools will block. Manual investigation required.

*Note: This runbook is strictly for local operational maintenance. This project DOES NOT connect to live brokers, DOES NOT send live financial orders, and DOES NOT provide investment advice.*
