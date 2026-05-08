# Research Quality Scorecard

The Research Quality Scorecard provides a centralized metric evaluating the overall research quality of the USA Signal Bot across its execution lifecycle. It computes a weighted score and assigns a status based on various internal system dimensions.

## Purpose

The scorecard answers the question: "How robust and credible are the results produced by the bot in its most recent run?"
It enforces a quantifiable measure of confidence before utilizing generated signals or strategies.

## Dimensions Evaluated

The scorecard aggregates scores from the following critical dimensions:
- **Data (10%):** Data freshness, cache presence, and universe coverage.
- **Feature (8%):** Pipeline generation status, warnings, and missing outputs.
- **Signal (10%):** Signal count, candidate selection, ranking output, and risk flags.
- **Backtest (12%):** Execution completeness, metric validity, and benchmark comparison presence.
- **Robustness (10%):** Walk-forward simulation, Monte Carlo execution, and parameter stability mapping.
- **Risk (10%):** Rejection balance, safety thresholds, and exposure warnings.
- **Portfolio (8%):** Basket presence and concentration guidelines.
- **Paper (10%):** Out-of-sample account simulation and drawdown constraints.
- **Comparison (10%):** Execution realism gaps and signal drift vs historical backtest.
- **Runtime (7%):** Execution status and encountered runtime errors.
- **Notification (3%):** Validation that the default telegram channel operates in Dry-Run Mode.
- **Documentation (2%):** Project compliance (README, docs, tests, and phase summaries).

## Scoring & Status Classification

A weighted sum calculates an `overall_score` (0.0 to 100.0).

- **PASS:** Score >= 75.0 with no critical issues.
- **WARN:** Score >= 50.0 but < 75.0, or if non-critical warnings are detected.
- **FAIL:** Score < 50.0, or if one or more critical issues are raised (e.g. missing signals).
- **INSUFFICIENT_DATA:** Important artifacts or directories are missing preventing evaluation.

**Disclaimer:** This score is exclusively an internal research indicator. It is **NOT** a guarantee of real-world profitability and must not be used as investment advice.

## CLI Usage

View configuration:
```bash
python -m usa_signal_bot quality-info
```

Generate scorecard:
```bash
python -m usa_signal_bot quality-scorecard --write
```
