# Guarded Pre-Paper Dry Rehearsal

The Guarded Pre-Paper Dry Rehearsal provides a strict, locally executed simulation environment to evaluate candidate configurations before they are permitted to undergo further readiness or paper-trading.

**IMPORTANT LIMITATIONS:**
- **This rehearsal is NOT an active paper trading activation.**
- **No paper state will be written or mutated.**
- **No live or demo broker orders will be generated or dispatched.**
- **No Telegram real-send notifications will be dispatched.**

## Features
1. **Read-Only Paper Baseline:** Operations are executed against a read-only snapshot of the current paper baseline, ensuring the real paper state remains unmutated.
2. **Deterministic Run:** Ensures stable and predictable dry runs without real-time side-effects.

## CLI Usage

Show the pre-paper rehearsal config:
```bash
python -m usa_signal_bot pre-paper-rehearsal-info
```

Generate the pre-paper dry rehearsal plan:
```bash
python -m usa_signal_bot pre-paper-plan --write
```

Execute the guarded pre-paper dry rehearsal run:
```bash
python -m usa_signal_bot pre-paper-dry-run --write
```
