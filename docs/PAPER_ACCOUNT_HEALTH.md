# Paper Account Health

The paper account health checks monitor the robustness of your virtual simulations:
1. **Cash Validations**: Alerts if cash becomes negative.
2. **Equity Validations**: Alerts if equity falls below 0.
3. **Ledger Consistency**: Verifies that cash ledger sums perfectly to the current account cash value.
4. **Drawdown Warning**: Alerts if max drawdown on virtual equity exceeds `max_drawdown_warning_pct` (default: 10%).

## Commands
To view the latest health report:
```bash
python -m usa_signal_bot paper-health-report --latest-paper
```
