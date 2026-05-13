# Delisting Awareness

## Overview
When analyzing historical pricing data, failing to realize a stock was delisted can lead to skewed risk/reward models. The **Delisting Awareness Checker** analyzes a symbol’s status alongside historical data anomalies to evaluate delisting risk.

## Detection Logic
The system combines two primary streams of evidence:
1. **Lifecycle Registry Lookups:** Checks if the symbol is explicitly marked as `DELISTED`, `ACQUIRED`, or `INACTIVE` in the local registry.
2. **Historical Data Checks:** If registry data is `UNKNOWN` or `ACTIVE` but historical pricing data is missing entirely, ends abruptly (stale), or has massive gaps, the delisting risk is artificially elevated.

## Risk Levels
- **Missing or Stale History:** Stale data (e.g., last traded 60 days ago) triggers a `HIGH` risk warning that the symbol may have been delisted.
- **Explicit Delisting:** Triggers `CRITICAL` risk if encountered during an active daily scan.

## CLI Usage
Check delisting risk for a specific symbol:
```bash
python -m usa_signal_bot delisting-awareness --symbol XYZ
```
Scan a loaded history file for stale symbols:
```bash
python -m usa_signal_bot stale-symbols
```

## Important Limitations
Missing or stale history is **evidence**, not proof. Many factors (e.g., API failures, local cache corruption) can cause stale data. Delisting awareness warnings require manual verification and should not be used for fully automated portfolio restructuring.
