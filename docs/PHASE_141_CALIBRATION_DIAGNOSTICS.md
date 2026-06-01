# Phase 141 - Calibration Diagnostics

Phase 141 performs calibration diagnostics, probability reliability review, and post-training validation on offline prediction artifacts.

## Overview
- **Input:** Phase 140 BaselineModelComparisonFullReview.
- **Goal:** Understand model reliability and calibration characteristics without performing calibration fitting.
- **Constraints:** Completely offline, no fitting, no threshold optimization, no deployment, no trade signals.

## Commands
```bash
python -m usa_signal_bot calibration-diagnostics-info
python -m usa_signal_bot resolve-calibration-inputs --write
python -m usa_signal_bot build-reliability-bins --write
python -m usa_signal_bot calculate-calibration-metrics --write
python -m usa_signal_bot calibration-diagnostics-review --write
```
