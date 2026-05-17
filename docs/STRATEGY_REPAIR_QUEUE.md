# Strategy Repair Queue

The Strategy Repair Queue acts as an incident and degradation triage list. It transforms diagnostic assessments, backtest failures, and attribution drags into actionable, tracked elements.

## Features
- **Triage & Deduplication**: Aggregates overlapping failure modes into a single repair item to avoid redundant experiments.
- **Priority Scoring**: Weights items based on the severity of the failure and the evidence quality. Critical signals automatically escalate in priority.
- **Scope Identification**: Resolves whether a degradation is isolated to a `SINGLE_STRATEGY`, generic across a `REGIME_BUCKET`, or affects `PORTFOLIO_LEVEL` sizing.

## Example CLI Usage
```bash
python -m usa_signal_bot research-workflow-info
python -m usa_signal_bot repair-queue --write
python -m usa_signal_bot repair-queue-triage --write
```
