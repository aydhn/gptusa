# Dry-Run Bridge Safety Guards

## Safety Checks
The system explicitly verifies that:
1. No paper state mutation occurs.
2. No paper or broker orders are generated.
3. No Telegram real sends happen.
4. No production configuration writes are allowed.
5. Active paper candidate enable is disabled.

## CLI Usage
```bash
python -m usa_signal_bot dry-run-risk-evaluate --write
python -m usa_signal_bot dry-run-bridge-validate --latest-review
```
