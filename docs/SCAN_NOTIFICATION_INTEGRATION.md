# Scan Notification Integration

The `NOTIFICATION` pipeline step integrates directly with the scan orchestrator to ensure seamless, event-driven alerts.

## Workflow

1. A market scan is executed (e.g., `scan-run-once --notify`).
2. The orchestrator triggers `run_notification` as the final optional step.
3. If `--notify` is provided, an `AlertEvaluationContext` is constructed from the `MarketScanResult`.
4. `AlertEvaluator` assesses the context against active `AlertPolicy` definitions.
5. If decisions yield `ROUTED`, `NotificationMessage`s are dispatched.
6. The `NotificationDispatcher` routes the message to the configured channel (defaulting to `dry_run`).

## CLI Usage

Example of executing a scan with notification routing in `dry_run`:

```bash
python -m usa_signal_bot scan-run-once --scope small_test_set --timeframes 1d --notify --notification-channel dry_run
```

The output paths for alert reports will automatically embed within the scan result output payload.
