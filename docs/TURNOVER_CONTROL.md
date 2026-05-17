# Turnover Control

## Overview
Rebalance plans are subject to absolute turnover constraints. Excessive turnover causes strategy decay from transaction costs and slippage.

## Features
- **Max Turnover Cap:** Suppresses low-priority actions (non-exits, smaller deltas) to ensure total turnover stays under the defined limit (e.g. 10% equity).
- **Dust Guard:** Ignores immaterial rebalance actions (e.g. < $25 deltas).
- **Cost-Aware Suppression:** Overlays transaction costs limits to review/suppress cost-heavy trades.

## CLI Usage
`python -m usa_signal_bot turnover-review --equity 100000`
`python -m usa_signal_bot dust-guard --delta-notional 10 --min-notional 25`
