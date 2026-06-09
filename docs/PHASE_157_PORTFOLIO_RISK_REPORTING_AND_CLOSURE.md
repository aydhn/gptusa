# Phase 157: Portfolio Risk Reporting and Closure

## Overview
Phase 157 acts strictly as a research-only local portfolio risk reporting, exposure governance, and portfolio band closure phase.
It securely ingests the outputs from Phase 156 and builds a final portfolio readiness gate for Phase 158.

## Constraints
- **Not Deployment:** This phase does not deploy trading bots.
- **Not Investment Advice:** All governance and risk outputs are for research only.
- **No Actual Allocations:** The `sandbox_optimizer_weight` field is not an `actual_target_weight` or `actual_allocation`.
- **No Live Trading:** Explicitly blocked from paper, live, broker execution, order generation, or state mutation.

## Usage
CLI commands available:
- `python -m usa_signal_bot portfolio-risk-info`
- `python -m usa_signal_bot build-portfolio-risk-summary --write`
- `python -m usa_signal_bot build-portfolio-band-compliance-audit --write`
- `python -m usa_signal_bot build-portfolio-band-closure-certificate --write`
- `python -m usa_signal_bot portfolio-risk-review --write`
