# Universe Sources

## What is a UniverseSource?
A `UniverseSource` is a strongly typed domain model representing a logical provider of ticker symbols. This abstraction allows the system to combine symbols from various places into a single, unified structure.

## Source Types
- `MANUAL_SEED`: Small, hardcoded test files or seeds.
- `USER_CSV`: The default watchlist or any explicitly managed local CSV.
- `LOCAL_IMPORT`: Large CSV files imported by the user into the `imports` directory.
- `PRESET`: Included starting templates (e.g., mega caps, sector ETFs).
- `SNAPSHOT`: A previously expanded and generated universe.
- `GENERATED`: Placeholder for dynamically computed lists (future).
- `RESERVED_EXTERNAL`: Placeholder for external API fetching (currently disabled).

## Why not fetch from the internet?
In Phase 11, the `RESERVED_EXTERNAL` source type is intentionally disabled.
1. **Web Scraping is Forbidden**: We do not parse DOM/HTML from financial sites.
2. **Reliability**: Relying on local CSVs guarantees the bot can always boot and scan.
3. **Data Quality Control**: A local import step forces the user to validate the list before the bot blindly requests price data for garbage symbols.

## Source Priority
Each source has a priority. During reconciliation (expansion), deterministic rules use this priority to decide which metadata wins if two sources provide the same symbol.
