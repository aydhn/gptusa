# Dry Admission Dossier Safety Guards

## Enforced Restrictions
The safety guards are responsible for catching and failing any dossier that breaches boundaries:
- **No active paper enable:** `activation_allowed` or `allows_active_paper` triggers block.
- **No paper admission:** `admission_allowed` triggers block.
- **No shadow launch / paper-mode launch:** `shadow_launch_allowed` / `paper_mode_launch_allowed` triggers block.
- **No rehearsal:** `rehearsal_allowed` or `paper_mode_rehearsal_allowed` triggers block.
- **No paper state mutation:** Any mutation keys or `allows_paper_state_mutation` triggers block.
- **No broker order:** Any real API routing or `allows_broker_execution` triggers block.
- **No Telegram real send:** `allows_telegram_real_send` triggers block.
- **No production config patch:** `allows_config_patch` triggers block.

If any rehearsal attempt is returned as `not blocked`, the overall safety check fails.

## CLI Examples
```bash
python -m usa_signal_bot dry-admission-dossier-continuity --write
python -m usa_signal_bot dry-admission-dossier-safety-check --write
python -m usa_signal_bot dry-admission-dossier-validate --latest-review
```
