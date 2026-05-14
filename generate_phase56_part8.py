import os
import re

def ensure_dir(file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

def write_file(file_path, content):
    ensure_dir(file_path)
    with open(file_path, 'w') as f:
        f.write(content)

# ---------------------------------------------------------
# DOCS
# ---------------------------------------------------------
docs_phase_56 = """
# Phase 56 Summary: Walk-Forward Cost Robustness, Slippage Stress Testing, and Execution Sensitivity Matrix

## Overview
Phase 56 introduces the Cost Robustness and Execution Sensitivity framework. This layer acts as an advanced, purely local heuristic filter to test walk-forward backtest results against various slippage, spread, impact, and fee stress scenarios. It helps identify strategies that only perform well under unrealistic cost assumptions.

## Key Features
- **Cost Stress Scenarios**: Built-in Baseline, Mild, Moderate, Severe, and Extreme cost scenarios.
- **Granular Stress Builders**: Specific multipliers for Slippage, Spread, Market Impact, Fee, Participation, and Liquidity Filters.
- **Fill Realism Modes**: Options to apply penalties or block fills (Optimistic to Strict).
- **Stressed Results Generation**: Net PnL recalculation based on stressed costs.
- **Execution Sensitivity Matrix**: A grid evaluating strategy performance across various combinations of cost friction.
- **Walk-Forward Cost Robustness**: Validating out-of-sample window survival under cost stress.
- **Fragility Detector & Breakeven Costs**: Identifying specific fragility reasons (e.g., "Profit Erased by Costs") and estimating the cost margin per trade.
- **Adapters**: Backtest, Basket Simulation, and Signal/Candidate adapters that attach non-destructive metadata.
- **Storage & Validation**: JSON storage for cost robustness reviews and strict validation to ensure no live broker/execution language is used.

## Limitations & Rules Enforced
- **NO BROKER API**: This phase does not integrate with Alpaca, IBKR, or any live/demo broker.
- **NO REAL FILL GUARANTEE**: All calculations are local heuristics.
- **NOT INVESTMENT ADVICE**: Outputs are solely for local operational analysis.
- **NO EXTERNAL TELEMETRY**: All reporting is local.
"""
write_file("docs/PHASE_56_SUMMARY.md", docs_phase_56)

docs_cost = """
# Cost Robustness Testing

## Purpose
Cost Robustness Testing evaluates how well a strategy's returns hold up when transaction costs are significantly worse than the baseline assumptions.

## Scenarios
- **Baseline**: 1.0x multipliers.
- **Mild**: 1.25x slippage/spread/impact.
- **Moderate**: 1.5x slippage/spread/impact, 1.25x fee.
- **Severe**: 2.0x slippage/spread/impact, 1.5x fee.
- **Extreme**: 3.0x slippage/spread/impact, 2.0x fee, Strict Fill Realism.

## Outputs
Gross vs. Stressed Net results, Failed Scenario counts, and a Cost Robustness Score.

## CLI Commands
`python -m usa_signal_bot cost-robustness-info`
`python -m usa_signal_bot cost-stress-scenarios`
`python -m usa_signal_bot cost-robustness-review --write`
"""
write_file("docs/COST_ROBUSTNESS_TESTING.md", docs_cost)

docs_slip = """
# Slippage Stress Testing

## Purpose
Simulates specific degradation in execution prices (slippage) to see if a strategy remains profitable.

## Modifiers
- Slippage Multipliers (e.g., 1.5x, 2.0x, 3.0x).
- Fill Realism Modes (Baseline, Conservative, Pessimistic, Strict).

## Warning
These tests are heuristics and do not replace real order book data.

## CLI Commands
`python -m usa_signal_bot slippage-stress --base-bps 20`
`python -m usa_signal_bot fill-realism-stress`
"""
write_file("docs/SLIPPAGE_STRESS_TESTING.md", docs_slip)

docs_sens = """
# Execution Sensitivity Matrix

## Purpose
Creates a multi-axis grid to find the exact thresholds where a strategy fails.

## Axes
- Slippage
- Spread
- Market Impact
- Fill Realism Mode

## Output
A matrix of cells showing Pass/Fail/Warn status based on net profitability.

## CLI Commands
`python -m usa_signal_bot sensitivity-matrix --write`
"""
write_file("docs/EXECUTION_SENSITIVITY_MATRIX.md", docs_sens)

docs_wf = """
# Walk-Forward Cost Robustness

## Purpose
Evaluates if the out-of-sample (OOS) windows of a walk-forward analysis survive cost stress.

## Logic
If more than a configurable percentage (e.g., 30%) of OOS windows become unprofitable under moderate stress, the strategy is marked as Fragile.

## CLI Commands
`python -m usa_signal_bot walk-forward-cost-robustness --write`
"""
write_file("docs/WALK_FORWARD_COST_ROBUSTNESS.md", docs_wf)

docs_frag = """
# Cost Fragility & Breakeven

## Cost Fragility
Detects why a strategy fails under stress:
- Profit Erased by Costs
- Sharpe Collapse
- Drawdown Expansion

## Breakeven Costs
Estimates the maximum transaction cost (in bps) a strategy can absorb before net PnL becomes zero.

## CLI Commands
`python -m usa_signal_bot cost-fragility --write`
`python -m usa_signal_bot breakeven-costs`
"""
write_file("docs/COST_FRAGILITY_AND_BREAKEVEN.md", docs_frag)

docs_limit = """
# Cost Robustness Limitations

1. **Heuristic Nature**: Stress scenarios are multipliers applied to estimated costs. They do not simulate actual market microstructure.
2. **No Order Book**: We do not replay Level 2 data.
3. **No Broker Fill Data**: We do not use live or demo accounts to verify fills.
4. **No Real Fee Schedules**: Fee stress uses proxies, not exact broker tiered schedules.
5. **Not Investment Advice**: A PASS status is an operational gate, NOT a live trading recommendation.
6. **No External Tools**: Strictly standard library and pandas.
"""
write_file("docs/COST_ROBUSTNESS_LIMITATIONS.md", docs_limit)
