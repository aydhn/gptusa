# Failure Recovery Workflow

## Overview
When an incident is logged, the Recovery Planner constructs a `RecoveryPlan`. This plan lists recommended recovery actions based on the incident's category (e.g., if a config error is detected, a config validation check is recommended).

## Safety Controls
- **Dry-run by default:** Plans are always generated and executed in dry-run mode unless specifically overridden.
- **Execute commands false by default:** `execute_commands_default` is set to `False` to prevent the system from autonomously running destructive CLI commands.
- **Critical incident blocking:** Incidents with `CRITICAL` or `BLOCKER` severities immediately halt automated recovery and mandate human manual review.

## CLI Commands
Generate and simulate a recovery plan:
```bash
python -m usa_signal_bot recovery-plan --latest-incident --write
python -m usa_signal_bot recovery-dry-run --latest-plan --write
```
