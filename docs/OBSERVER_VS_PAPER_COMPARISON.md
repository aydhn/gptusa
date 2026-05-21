# Observer vs Paper Comparison
Compares locked observer runtime outputs with local paper snapshots read-only without executing any orders.

## Purpose
Ensure observer signals match paper state gracefully.

## CLI Usage
```bash
python -m usa_signal_bot observer-paper-compare --write
python -m usa_signal_bot observer-signal-delta --write
python -m usa_signal_bot observer-drift-delta --write
```
