# Volume Participation and Slippage Proxy

Estimates execution cost (`spread_proxy_bps`, `slippage_proxy_bps`) and tests order size viability (`participation_rate_pct`). High participation increases slippage drastically or blocks the trade.

## Example Usage
```bash
python -m usa_signal_bot participation-check --notional 1000 --avg-dollar-volume 1000000
python -m usa_signal_bot slippage-proxy --symbol SPY --notional 1000
```
