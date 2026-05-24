# Board Dossier Safety Guards

## Security Principles
- No active paper enable.
- No paper admission.
- No shadow launch.
- No paper-mode launch.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.

## Blocking Conditions
Any of the following will block the dossier:
- `shadow_launch_allowed`=True
- `admission_allowed`=True
- `mutation_detected`=True
- `order_created`=True
- Missing `all_writes_blocked`=True
- Attempt not blocked by shadow-launch rules

## CLI Usage
```bash
python -m usa_signal_bot board-dossier-continuity --write
python -m usa_signal_bot board-dossier-safety-check --write
python -m usa_signal_bot board-dossier-validate --latest-review
```
