# Active Universe

The active universe represents the definitive list of symbols (stocks and ETFs) that the bot will process for data downloading, feature engineering, and signal generation.

## Active Snapshot
An active universe is typically resolved from an "Active Snapshot"—a frozen, validated universe state. Using a snapshot guarantees that the data pipeline runs on a stable, reproducible set of symbols.

## Resolver Precedence
When resolving the active universe, the system checks sources in the following order:
1. **Explicit File:** If a specific local file is passed (e.g., via CLI).
2. **Active Snapshot:** The snapshot currently marked as active.
3. **Latest Snapshot:** The most recently created snapshot (if fallback is enabled).
4. **Default Watchlist:** The baseline fallback watchlist.

## Commands
- `python -m usa_signal_bot active-universe-info`: View current active universe resolution.
- `python -m usa_signal_bot active-universe-symbols --limit 20`: List symbols in the active universe.
- `python -m usa_signal_bot universe-activate-snapshot --snapshot-id <id>`: Mark a snapshot as active.
