# Telegram Notifications

## Purpose
The Telegram Notification system provides a secure, log-only/dry-run default way to output local research findings to Telegram.

## Safety & Security Defaults
- **Real Send Disabled:** `telegram.enabled` and `telegram.allow_real_send` are strictly `false` by default.
- **Dry Run Mode:** Telegram operates in `dry_run=true` matching the orchestrator's safe isolation rules.
- **No Investment Advice:** Telegram messages are explicitly tagged to prevent any "advice" classification.
- **Token Security:** Environment variables (`USA_SIGNAL_BOT_TELEGRAM_TOKEN`) are used to prevent file leakage. The logs always heavily redact tokens automatically.

## Broker Isolation
The notification system is strictly one-way and cannot create broker or live paper trading orders.

## CLI Usage
Check your telegram configuration and redact properties:
`python -m usa_signal_bot telegram-status`

Test connectivity safely via dry run:
`python -m usa_signal_bot notification-send-test`
