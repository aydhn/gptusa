# Production Readiness Gate

The Production Readiness Gate is a strict evaluation layer designed to verify that the local system satisfies the required pre-requisites for safe, simulated portfolio research operations.

## Purpose

The Readiness Gate examines the Research Quality Scorecard and artifact index against predefined thresholds and safety constraints, deciding if the run can proceed. It enforces local bounds ensuring the bot does not operate outside safety guardrails.

## Gate Rules

The gate evaluates a list of rules that dictate its final status:

1. **Overall Score Threshold:** Must be >= 70.0.
2. **No Critical Issues:** Critical errors must evaluate to 0.
3. **Data Quality Threshold:** Must be >= 50.0.
4. **Backtest Quality Threshold:** Must be >= 50.0.
5. **Risk Quality Threshold:** Must be >= 50.0.
6. **Paper Quality Threshold (if applicable):** Must be >= 40.0.
7. **Comparison Quality Threshold (if applicable):** Must be >= 40.0.

## Gate Statuses

- **PASSED:** All mandatory rules satisfied.
- **WARNING:** Non-critical violations exist.
- **FAILED:** A mandatory threshold or standard rule failed.
- **BLOCKED:** The system contains a CRITICAL violation or explicit configuration violating the system constraints (e.g., Live broker flags active, Telegram default real sends active).

**Disclaimer:** "PASSED" dictates readiness strictly within a local historical research or simulated paper context. This evaluation does not imply the code is ready for real money or live broker execution.

## CLI Usage

```bash
python -m usa_signal_bot readiness-gate --scope full_local_stack --write
```
