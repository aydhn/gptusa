# Paper Notification Reporting

This document explains how notifications are generated for Paper runtime and daily reporting events.

## Notification Generation
The local paper engine utilizes `NotificationMessage`s to inform you about paper activities. Available paper notifications include:
- `PAPER_RUN_SUMMARY`: Generated immediately upon completing a paper runtime cycle. Contains intents vs fills counts.
- `PAPER_DAILY_ACCOUNT_REPORT`: A comprehensive summary of starting vs ending cash/equity, open positions, open trades, and total PnL.
- `PAPER_ACCOUNT_HEALTH`: Alerts sent if paper cash goes negative or drawdowns exceed thresholds.
- `PAPER_RECONCILIATION_WARNING`: Triggered when equity calculations do not match expected market values of positions.

## Disclaimers & Safety
These notifications are handled entirely by the `dry_run` or `log_only` adapters by default. Telegram actual dispatches are turned OFF. Nothing generated here constitutes an actual trade alert or investment advice.
