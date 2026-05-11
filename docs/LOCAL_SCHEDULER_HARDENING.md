# Local Scheduler Hardening

## Overview
Phase 47 hardens the local operations with a robust scheduling and locking infrastructure. The design avoids reliance on external execution or daemons, utilizing run-once and dry-run mechanisms exclusively for safety.

## Run-Once and Dry-Run Mechanisms
The execution paradigm defaults to simulated runs (dry-run). Active jobs can only execute commands defined within an explicit, safe allowlist, preventing unintended destructive behavior.

## Safe Allowlist & Blocked Commands
- Valid commands include safe read-only reporting tasks (e.g., `smoke`, `health`, `observability-info`).
- Destructive commands like `cleanup-execute`, `rollback-execute`, and live broker orders are strictly blocked.

## CLI Examples
- `python -m usa_signal_bot scheduler-info`
- `python -m usa_signal_bot scheduler-plan --dry-run --write`
- `python -m usa_signal_bot scheduler-run-once --dry-run --write`
