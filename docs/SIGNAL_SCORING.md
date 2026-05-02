# Signal Scoring

## Overview
Signal Scoring evaluates the internal quality and structural completeness of a generated `StrategySignal`. The purpose of signal scoring is *not* to override a strategy's predictive confidence, but to determine whether the signal structure is robust enough to be considered a viable candidate.

A score ranges from `0.0` to `100.0`.

> **Important Constraint:** In the current phase (Phase 22), the system operates entirely without backtests or live execution. Therefore, the maximum attainable score for any signal is intentionally capped (e.g., `70.0`). A score does not constitute trade execution or financial advice.

## Core Components
- **Base Score:** The minimum score granted for a generated strategy.
- **Confidence Contribution:** Scaled addition based on the underlying strategy's `confidence` level.
- **Reason Quality:** Bonus score based on the presence and structure of text reasons explaining the signal's logic.
- **Feature Snapshot Quality:** Bonus score ensuring the signal explicitly contains the data features it was evaluated on.
- **Risk Penalty:** Deductions applied if the signal exhibits high risk flags (e.g., insufficient features, data quality warnings).

## Confidence vs. Score
- **Confidence (`0.0 - 1.0`):** Represents the strategy algorithm's internal belief that the target movement will occur.
- **Score (`0.0 - 100.0`):** Represents the architectural and structural robustness of the signal itself.

## Example CLI Usage

You can score a previously generated JSONL signal file using the CLI:

```bash
python -m usa_signal_bot signal-score-file --file data/signals/example.jsonl --write
```
