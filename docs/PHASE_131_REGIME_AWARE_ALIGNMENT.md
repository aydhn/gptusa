# Phase 131: Regime-Aware Feature/Factor Alignment

This phase ingests the `MarketBehaviorFullReview` from Phase 130 in read-only mode and aligns the frozen feature/factor artifact chain with regime behavior and reports.

## Features
- Ingests Phase 130 artifacts.
- Validates that no model training, prediction, strategy activation, or deployment occurs.
- Extracts behaviors and applies regime-context mapping.

## Usage
- `python -m usa_signal_bot regime-alignment-info`
- `python -m usa_signal_bot compute-regime-compatibility --write`
- `python -m usa_signal_bot regime-alignment-review --write`
