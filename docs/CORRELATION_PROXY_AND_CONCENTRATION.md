# Correlation Proxy and Concentration

Since downloading full correlation matrices can be expensive or slow, we use a heuristic proxy based on shared metadata (sectors, clusters).

## Heuristics
- **Same Symbol**: VERY HIGH risk
- **Same Cluster**: HIGH risk
- **Same Sector**: MODERATE risk

Concentration guards evaluate exposures against configurable percentage thresholds (e.g., max 10% per symbol).

## Example CLI Commands
```bash
python -m usa_signal_bot correlation-proxy --symbols AAPL,MSFT,NVDA
python -m usa_signal_bot concentration-review --equity 100000
```
