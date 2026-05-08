# Regression Limitations

- **Synthetic Data Only**: Regression fixtures do not reflect real market conditions or anomalies.
- **No Performance Guarantee**: A PASS means the Python code executed without error. It provides zero guarantees on profitability or strategy alpha.
- **No Broker Execution**: Live, paper, or demo broker routing is strictly prohibited and physically un-implemented in this layer.
- **No Network Requests**: The regression harness operates offline.
- **Drift is Not Always a Bug**: Changes in code (e.g., adding a new feature) will intentionally alter snapshots. Use `--update-baseline` deliberately.
- **Not Investment Advice**: Outputs and reports from the harness are for software engineering validation only.
