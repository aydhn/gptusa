# Dry-Run Bridge Limitations

- **Not Active Paper Trading**: The dry-run bridge evaluates candidates but does not make them active.
- **Proposals are Not Orders**: Generated `DryRunProposal`s are hypothetical intents, not actual trading orders.
- **Human Checkpoints are Not Approvals**: Passing a checkpoint does not grant deployment approval.
- **Telemetry is Local**: Telemetry data is only stored locally and not exported.
- **Read-Only Snapshot**: The paper snapshot used during evaluation is strictly read-only.
- **No API Execution**: Broker APIs, real/demo execution, Telegram live dispatch, and configuration patching are completely excluded.
- **Not Investment Advice**: The output of the bridge is purely operational and not financial advice.
