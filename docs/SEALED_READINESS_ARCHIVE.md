# Sealed Readiness Archive

The sealed readiness archive aggregates all evidence (promotion dossier, rehearsals, safety boards) into an immutable metadata package.

**Important Limitations:**
- The archive is NOT a deployment package.
- It does NOT authorize live, demo, or paper trading.

CLI Usage:
```
python -m usa_signal_bot sealed-archive-manifest --write
python -m usa_signal_bot sealed-archive-seal --write
python -m usa_signal_bot sealed-archive-integrity --write
```
