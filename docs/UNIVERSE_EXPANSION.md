# Universe Expansion

Universe Expansion is the process of reading multiple `UniverseSource` items, merging them, resolving conflicts, and writing the result as a point-in-time Snapshot.

## Layer Logic
The system categorizes sources by layer. When expanding, you can filter which layers to include:
- `CORE`, `WATCHLIST`, `MEGA_CAP`, `SECTOR_ETF`, `INDEX_ETF`, `CUSTOM`, `RESEARCH`, `CANDIDATE`, `EXCLUDED`

## Conflict Resolution
When multiple sources contain the same symbol (e.g., `AAPL` in the watchlist and `AAPL` in an imported S&P500 list), the system must reconcile them:
- `PREFER_COMPLETE_METADATA`: Keeps the symbol definition with the most populated fields (sector, industry, etc.).
- `PREFER_ACTIVE`: Prioritizes an active symbol over an inactive one.
- `FIRST_WINS` / `LAST_WINS`: Uses deterministic priority ordering.
- `ERROR_ON_CONFLICT`: Halts expansion if a discrepancy is found (strict mode).

## Snapshot Creation
Every successful expansion creates a versioned Snapshot (`snapshot_id`), a Summary JSON, a Validation Report, and a Reconciliation Report.

## CLI Commands
```bash
python -m usa_signal_bot universe-sources
python -m usa_signal_bot universe-import --file my_symbols.csv --name my_custom_list
python -m usa_signal_bot universe-expand --include-layers CORE,WATCHLIST,CUSTOM --max-symbols 200
python -m usa_signal_bot universe-snapshots
```
