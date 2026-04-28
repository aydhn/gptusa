# USA Signal Bot Configuration

## Configuration Files

The project relies on two main configuration files:

1. **`default.yaml`**: This file contains the default system-wide settings. It is committed to version control and serves as the baseline configuration for the application.
2. **`local.yaml`**: This file overrides specific values from `default.yaml` for a local environment. **It is excluded from git tracking (`.gitignore`).** You should create this file by copying `local.example.yaml` to tailor the bot for your own setup without risking committing sensitive or environment-specific data.

## Configuration Merge Logic

When the bot starts up, it utilizes a deeply nested merging logic (`deep_merge_dicts`):
1. Loads the `default.yaml`.
2. Loads the `local.yaml` (if it exists).
3. The `local.yaml` settings are applied over the `default.yaml`.
4. Values explicitly defined in `local.yaml` override `default.yaml`. Values omitted in `local.yaml` remain intact from `default.yaml`.

## Forbidden Settings

To strictly enforce that this bot remains a local paper-trading simulation without exposing live APIs or web endpoints, certain configuration states are actively guarded and validated. Attempting to override them will throw a fatal `ConfigError`:
- `runtime.mode` must equal `"local_paper_only"`.
- `runtime.broker_order_routing_enabled` must be `false`.
- `runtime.web_scraping_allowed` must be `false`.
- `runtime.dashboard_enabled` must be `false`.

## Important Categories

### Risk Management (`risk`)
- `max_position_pct`: Maximum allocation for a single position as a ratio (e.g., `0.10` = 10%).
- `max_total_exposure_pct`: The total allowable portfolio exposure (e.g., `0.80` = 80%).
- `max_daily_loss_pct`: Threshold limit for daily paper-trading loss.

### Universe Filtering (`universe`)
Defines the pool of assets to scan.
- `include_stocks`, `include_etfs`: Toggles for asset types.
- `min_price`: Filters out penny stocks.
- `max_symbols_per_scan`: Limits the total number of tickers analyzed simultaneously to prevent out-of-memory or rate-limit issues.

### Telegram (`telegram`)
The bot reads the *names* of the environment variables from the configuration (e.g., `"TELEGRAM_BOT_TOKEN"`) rather than the tokens themselves. See `ENVIRONMENT.md` for instructions on securely setting environment variables.
