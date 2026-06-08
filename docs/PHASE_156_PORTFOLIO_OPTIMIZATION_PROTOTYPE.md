# Phase 156: Portfolio Optimization Prototype

Phase 156 is a completely offline, read-only research layer designed to construct and evaluate portfolio optimization prototypes without activating strategy deployments or placing real broker trades.

## Key Objectives
- Read-only ingestion of Phase 155 artifacts (`PortfolioConstructionFullReview`).
- Constructing offline Sandbox candidates.
- Generating optimizer configurations:
  - Equal baseline
  - Score maximizing
  - Risk budget aware
  - Concentration minimizing
  - Robustness first
  - Turnover aware
- Comparing these optimizer allocations through Objective Score models.
- Evaluating strict non-execution boundaries.

## Forbidden Actions
- Live/Demo/Paper trade execution or order mutation.
- Broker integration.
- True capital deployments (`capital_allocation`).
- Real `target_weight` production. Outputs are strictly `sandbox_optimizer_weight`.
- Deployment and background task scheduling.

## CLI Usage
```bash
python -m usa_signal_bot optimizer-prototype-info
python -m usa_signal_bot build-optimizer-policy --write
python -m usa_signal_bot build-score-maximizing-optimizer --write
python -m usa_signal_bot build-objective-comparison-report --write
python -m usa_signal_bot optimizer-prototype-review --write
```
