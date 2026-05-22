# Paper Mode Simulation Preflight

## Purpose
The Paper-mode simulation preflight checks if the paper-mode setup functions without trying to mutate any state or trigger executions.

## Disclaimer
Preflight is not the real paper runtime.

## No-write Simulation Steps
1. read_only_snapshot_load
2. candidate_metadata_load
3. signal_pipeline_dry_preview
4. risk_pipeline_dry_preview
5. notification_dry_preview
6. write_lock_assertion
7. activation_firewall_replay_reference
8. no_write_summary

## Runtime Write-Lock Assertion
The runtime write lock verifies that all writes remain blocked throughout the simulated timeframe.

## CLI Examples
- `python -m usa_signal_bot paper-mode-preflight-plan --write`
- `python -m usa_signal_bot paper-mode-preflight-run --write`
- `python -m usa_signal_bot no-write-invariant-check --write`
