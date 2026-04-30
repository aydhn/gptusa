# Active Universe

## What is the Active Universe?
The "Active Universe" is the single, authoritative source of symbols currently selected for trading or research. It acts as the gateway between symbol management (Phase 11) and the data download pipeline (Phase 12).

## What is an Active Snapshot?
An "Active Snapshot" is a specific universe snapshot that has been explicitly marked as `ACTIVE`. This allows researchers to freeze a large universe, review it, and then "activate" it so that all subsequent data runs pull from exactly that list.

## Resolver Order
When the data pipeline needs to know what symbols to download, it uses the Active Universe Resolver, which follows this priority order:
1. **Explicit File**: If a user passes `--file` to the CLI, it uses that exact local CSV.
2. **Active Snapshot**: The snapshot marked `ACTIVE` in `data/universe/catalog/active_snapshot.json`.
3. **Latest Snapshot**: If no active snapshot exists, it falls back to the most recently created snapshot.
4. **Default Watchlist Fallback**: If no snapshots exist, it gracefully falls back to `data/universe/watchlist.csv`.

## Active Universe vs. Watchlist
- **Watchlist**: A small, static seed list of symbols.
- **Active Universe**: A potentially massive, multi-source aggregated list (from presets or imports) that represents the full scope of the trading system at a given point in time.

## CLI Examples

View current active universe resolution logic:
```bash
python -m usa_signal_bot active-universe-info
```

List the symbols in the active universe:
```bash
python -m usa_signal_bot active-universe-symbols --limit 20
```

Activate a specific snapshot:
```bash
python -m usa_signal_bot universe-activate-snapshot --snapshot-id expanded_universe_2026...
```
