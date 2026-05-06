# Alert System Limitations

The notification and alert architecture is built to ensure safe, localized research usage. The following strict limitations apply:

1. **Not Investment Advice:** Alerts are informational snapshots based on historical evaluation rules and do not constitute financial advice.
2. **No Execution Capability:** The Alert Policy Layer does not and cannot create, route, or execute live, paper, or demo broker orders.
3. **No Telegram Interaction:** The Telegram integration is an outbound-only sender. It does not provide webhook listeners or interactive bot commands.
4. **Disabled by Default:** Telegram real sending (`allow_real_send`) is explicitly disabled by default. All notifications default to `dry_run` or `log_only`.
5. **Basic Suppression:** Duplicate and cooldown logic is local state management; it does not replace robust rate-limiting edge architectures, though it protects against local loop errors.
6. **No Dashboards:** This layer exposes evaluation outputs solely via local CLI (`alert-latest`, `alert-summary`) and JSON/L files.
