# Bridge Replay Audit Seal

## Purpose
The Bridge Replay Audit Seal verifies that no dangerous routes were allowed during the bridge execution and that the replay passed.

## Requirements
- `seal` must be metadata-only
- `dangerous_allowed_count=0`
- `all_dangerous_routes_denied=true`

## CLI Usage
- `python -m usa_signal_bot bridge-replay-audit-seal --write`
- `python -m usa_signal_bot bridge-replay-seal-validate --write`
