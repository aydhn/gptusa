# Acceptance Board Seal

## Purpose
The Acceptance Board Seal creates an immutable, metadata-only hash reflecting that all non-execution board boundaries have been met.

## METADATA ONLY
The Acceptance Board Seal is strictly metadata. It does NOT:
- Grant execution permission
- Grant paper mode or shadow launch permissions
- Change the paper configuration

## Accepted Boundaries
- `non_execution_board_valid`
- `runtime_map_replay_passed`
- `all_dangerous_runtime_routes_denied`
- `non_execution_seal_integrity_valid`

## CLI Usage
```bash
python -m usa_signal_bot acceptance-board-seal --write
python -m usa_signal_bot acceptance-board-seal-validate --write
```
