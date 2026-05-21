# Observer Governance Safety Guards
Guards preventing active execution during observer governance.

- No active paper enable
- No paper state mutation
- No paper order
- No broker order
- No Telegram real send
- No production config patch
- Locked runtime confirmed

## CLI Usage
```bash
python -m usa_signal_bot observer-safety-compliance --write
python -m usa_signal_bot observer-governance-validate --latest-review
```
