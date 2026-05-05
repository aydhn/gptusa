# Portfolio Construction

This document details the portfolio construction layer established in Phase 32. This layer bridges the gap between risk evaluation/candidate selection and portfolio building.

## Purpose
The primary goal is to convert `RiskDecision` and `SelectedCandidate` objects into `PortfolioCandidate` objects, allocate target weights across them using baseline methods, and produce a `PortfolioBasket` while strictly adhering to limits.

## Models
1. **PortfolioCandidate**: The standardized candidate containing symbol, timeframe, score info, action, approved notional limits, and status.
2. **AllocationRequest**: Captures equity, available cash, allocation method, limits, and the candidates to process.
3. **AllocationResult**: Contains target weight, notional, and quantity assignments alongside caps/reductions applied.
4. **PortfolioBasket**: A container of candidates, their finalized allocations, and the remaining cash buffer, assigned a `PortfolioReviewStatus`.
5. **PortfolioConstructionResult**: The ultimate record of the run, encompassing the basket, allocations, risk budgeting reports, and concentration checks.

## Process
`RiskDecisions` generated from the `RiskEngine` represent "approved limits" per symbol/strategy/timeframe. These are mapped into `PortfolioCandidate` models where eligible allocations are calculated based on the requested baseline method (like equal weight, or notional-from-risk-decision). It calculates normalized raw weights, enforces candidate caps, group caps (via concentration guards), then produces a basket.

If concentration limits or risk budget limits are breached, the basket is marked with `NEEDS_REVIEW`.

## Key Limitations (Phase 32)
- **NOT an Optimizer**: No optimization logic (Mean-Variance, Kelly criterion, efficient frontier) exists here.
- **NOT Investment Advice**: Portfolio output metrics are built purely to fuel downstream simulation and research operations.
- **NO Broker Execution**: Generating an `AllocationResult` or `PortfolioBasket` implies simulated holding limits, it does not interact with a broker, paper trade facility, or live API.

## CLI Usage

View current configuration limits:
```bash
python -m usa_signal_bot portfolio-info
```

Build a portfolio from the most recent risk decision engine output:
```bash
python -m usa_signal_bot portfolio-build-from-risk --latest-risk --equity 100000 --cash 100000 --method notional_from_risk_decision --write
```
