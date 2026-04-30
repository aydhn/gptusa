# Universe Catalog

The Universe Catalog is the central registry for all universe assets available to the bot.

## What it tracks
- `UniverseSource` definitions (default watchlist, presets).
- Imported user CSVs.
- Generated Snapshots.
- The pointer to the currently **Active Snapshot**.

## Activating a Snapshot
When an expansion occurs, it generates a snapshot, but doesn't necessarily make it the active default. You activate it via CLI, updating `active_snapshot.json`.

## Exporting
The export system pulls from the currently Active Snapshot (or falls back to the default watchlist) and can generate:
- CSVs (Full standard schema)
- JSON
- TXT (Simple newline-separated lists for copy/pasting)

## CLI Commands
```bash
python -m usa_signal_bot universe-catalog
python -m usa_signal_bot universe-activate-snapshot --snapshot-id <id>
python -m usa_signal_bot universe-export --format txt --active-only
```
