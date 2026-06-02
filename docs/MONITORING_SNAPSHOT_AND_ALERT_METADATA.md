# MONITORING_SNAPSHOT_AND_ALERT_METADATA

## Monitoring Snapshot
The `MonitoringSnapshotSpec` aggregates all calculated drift metrics into a cohesive, deterministic snapshot.

## Alert Rule Metadata
The `DriftAlertRuleMetadata` defines thresholds and trigger conditions based on the drift metrics.

### Critical Safety Guard
- `notification_preview_only = True`
- `alert_sender_enabled = False`
- `telegram_real_send_enabled = False`

The alert rules are templates for human review and simulated workflows. They **do not** interact with the Telegram bot or any external notification service.
