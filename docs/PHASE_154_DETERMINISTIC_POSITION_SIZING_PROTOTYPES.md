# Phase 154: Deterministic Position Sizing Prototypes, Sizing Diagnostics and Safety Validation

Phase 154 completes the integration and implementation of a deterministic position sizing prototyping system.

## Overview
Phase 154 is a **research-only deterministic sizing prototype phase**. It explicitly does **not** perform actual portfolio construction, target weight generation, allocation, capital deployment, live trading, paper trading, or real broker execution.
This phase ingests the PortfolioFoundationFullReview outputs from Phase 153 to resolve inputs and apply sizing boundary prototypes via various methods (e.g., fixed-fractional, volatility-adjusted, drawdown-adjusted, cost-aware).

## Core Responsibilities
- Ingest `PortfolioFoundationFullReview` securely.
- Resolve sizing inputs and candidate universe boundaries.
- Build sizing policies and method contracts.
- Calculate research-only deterministic prototypes: Fixed-Fractional, Volatility-Adjusted, Drawdown-Adjusted, Cost-Aware, Liquidity-Aware, and Robustness-Adjusted.
- Apply Cap/Floor boundaries.
- Generate comparison matrices and diagnostics (disagreement, cap/floor bindings, sensitivity, risk budget adherence).
- Perform strict safety and readiness checks prior to proceeding to Phase 155.

## CLI Usage
Phase 154 introduces several safe commands. They do not trigger real API calls or trade executions.
```bash
python -m usa_signal_bot sizing-prototype-info
python -m usa_signal_bot build-sizing-policy --write
python -m usa_signal_bot build-fixed-fractional-sizing --write
python -m usa_signal_bot build-sizing-comparison-matrix --write
python -m usa_signal_bot sizing-prototype-review --write
```

## Readiness Gate
A `ready_for_phase155=true` result signifies only that the sandbox boundaries, policies, methods, schemas, and prototype outputs passed validations ensuring they produce NO execution artifacts. It serves as an authorization strictly for the Phase 155 portfolio constraint-aware allocation sandbox coding.
