# Pre-Paper Readiness Evidence Refresh

Collects and validates that all required pre-paper evidence is fresh before allowing readiness decision.

## Key Principles
- **Evidence Gap:** Checks for missing or stale evidence.
- **Required Evidence:** Final handoff, replay result, zero mutation audit, etc.
- **Not an activation:** Collecting evidence does not approve live trading.

## Commands
```bash
python -m usa_signal_bot pre-paper-evidence-collect --write
python -m usa_signal_bot pre-paper-evidence-refresh --write
python -m usa_signal_bot pre-paper-evidence-gaps --write
```
