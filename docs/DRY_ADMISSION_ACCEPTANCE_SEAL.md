# Dry Admission Acceptance Seal

## Purpose
The Acceptance Seal cryptographically and logically binds the success of prior dry admission gates (shadow replay, evidence freeze). It acts as a metadata artifact proving that the strict non-execution boundaries were passed.

## Crucial Note
**The Dry-Admission Acceptance Seal is METADATA-ONLY. It is NOT an active paper, live, demo, or rehearsal approval.**
By design, the seal ensures that no real operations are permitted (`allows_rehearsal=false`, `allows_broker_execution=false`).

## Accepted Boundaries
- dry_admission_gate_passed
- shadow_replay_passed
- board_evidence_freeze_valid
- no_shadow_launch_permission
- no_paper_mode_launch_permission
- no_rehearsal_permission
- no_paper_admission_permission
- no_order_creation
- no_paper_state_write
- no_broker_execution
- no_config_patch
- no_telegram_real_send
- not_investment_advice

## CLI Examples
```bash
python -m usa_signal_bot dry-admission-acceptance-seal --write
python -m usa_signal_bot dry-admission-acceptance-seal-validate --write
```
