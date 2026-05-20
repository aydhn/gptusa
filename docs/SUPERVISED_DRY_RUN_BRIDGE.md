# Supervised Dry-Run Bridge

The `SupervisedDryRunBridgePlan` defines how a quarantined candidate will be evaluated against the current paper state without actually modifying anything.

## Purpose
To allow a candidate to generate theoretical signals/intents and compare them to a read-only snapshot of the active paper state, depositing the results in an isolated directory.

## Operations
**Allowed:**
* `READ_PROMOTION_TICKET`
* `READ_CANDIDATE_BUNDLE`
* `READ_SHADOW_GOVERNANCE`
* `READ_PAPER_SNAPSHOT`
* `BUILD_DRY_RUN_PLAN`
* `WRITE_QUARANTINE_OUTPUT`
* `GENERATE_NOTIFICATION_PREVIEW`

**Denied (Always):**
* `WRITE_PAPER_STATE`
* `SEND_PAPER_ORDER`
* `SEND_BROKER_ORDER`
* `SEND_TELEGRAM_REAL`
* `WRITE_PRODUCTION_CONFIG`

## Output Isolation
All bridge outputs are strictly written to `data/paper_quarantine/outputs/`. Path traversal, writing to `data/paper/`, or modifying `config/` is actively blocked.

## CLI Examples
```bash
python -m usa_signal_bot dry-run-bridge-plan --write
python -m usa_signal_bot bridge-operation-guard --operation send_paper_order
python -m usa_signal_bot bridge-validate --write
```
