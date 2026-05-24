# Paper Readiness Non-Execution Board Dossier

## Purpose
The Paper-Readiness Non-Execution Board Dossier compiles all metadata, evidence, and safety assertions from the non-execution phase into a sealed, immutable metadata record.

## NOT AN APPROVAL
This dossier is strictly a metadata collection layer. It does NOT:
- Activate paper trading
- Start a paper mode simulation
- Mutate the local paper state
- Create paper or broker orders
- Send real Telegram messages
- Patch production configurations

## Required Evidence
The dossier verifies the presence of:
- `paper_readiness_non_execution_board`
- `runtime_map_replay_result`
- `non_execution_seal_integrity_audit`

## CLI Usage
```bash
python -m usa_signal_bot board-dossier-evidence --write
python -m usa_signal_bot board-dossier --write
python -m usa_signal_bot board-dossier-review --write
```
