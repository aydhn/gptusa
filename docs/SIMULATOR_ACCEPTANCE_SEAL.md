# Simulator Acceptance Seal

## Purpose
The Simulator Acceptance Seal is a strict boundary-setting metadata artifact that records the evaluation of the Simulator Gate Dossier.

## Restrictions
- It is metadata-only.
- It does **not** grant active paper, live, demo, or sandbox runtime admission approval.

## Accepted Boundaries
- simulator_gate_passed
- rehearsal_replay_passed
- dry_admission_evidence_freeze_valid
- no_simulator_admission_permission
- no_local_paper_simulator_permission
- no_sandbox_runtime_admission_permission
- no_paper_sandbox_runtime_permission
- no_paper_admission_permission
- no_order_creation
- no_paper_state_write
- no_broker_execution
- no_config_patch
- no_telegram_real_send
- not_investment_advice

## CLI Examples
`python -m usa_signal_bot simulator-acceptance-seal --write`
`python -m usa_signal_bot simulator-acceptance-seal-validate --write`
