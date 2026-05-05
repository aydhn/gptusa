# Risk Engine

The Risk Engine serves as the core foundational layer for evaluating candidate signals against risk constraints within the USA Signal Bot ecosystem.

## Purpose
The primary objective of the Risk Engine is to assess incoming `CandidateRiskInput` signals and provide an isolated, deterministic decision on their viability based on configured position sizing and exposure constraints. **It is essential to understand that Risk Approval is strictly for research, backtest, and paper environments.** It is *not* a live trade approval system, and no broker routing or execution occurs from this module.

## Core Models

### Candidate Risk Input
The `CandidateRiskInput` is an adapter model translating `StrategySignal` or `SelectedCandidate` objects into standardized data (price, confidence, rank score, volatility, etc.) that the risk engine understands.

### Risk Decision
The outcome of the Risk Engine is a `RiskDecision`. It encompasses:
- `status`: APPROVED, REJECTED, REDUCED, or NEEDS_REVIEW.
- `approved_quantity` / `approved_notional`: The final position sizing authorized.
- `checks`: Comprehensive results for each evaluated constraint.
- `risk_score`: A quantifiable 0-100 metric assessing the signal's overall risk profile.

### Risk Score & Checks
Every candidate undergoes thorough verification:
- Valid Price
- Cash Buffer validation
- Max Position Notional bounds
- Shorting limitations
- Portfolio / Symbol / Strategy Exposure limitations
A penalty is applied for each failed or warned check, generating a `risk_score`. Critical issues result in a `REJECTED` status.

## CLI Commands
- Display the configuration:
  `python -m usa_signal_bot risk-info`
- Evaluate a set of selected candidates:
  `python -m usa_signal_bot risk-evaluate-candidates --file data/signals/ranking/selected_candidates.jsonl --equity 100000 --cash 100000 --write`
