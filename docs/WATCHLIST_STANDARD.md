# Watchlist CSV Standard

The USA Signal Bot uses a strict CSV schema for managing symbols.

## Required Columns
- `symbol`: The trading ticker (e.g., AAPL, SPY, BRK.B). Must be alphanumeric with optional dots or hyphens. No spaces allowed.
- `asset_type`: Must be exactly `stock` or `etf`.

## Optional Columns
- `name`: Full name of the asset.
- `exchange`: Exchange where it trades (e.g., NASDAQ, NYSE).
- `currency`: Defaults to USD.
- `active`: Boolean indicating if the symbol should be scanned (true/false). Defaults to true.
- `sector`: GICS sector (e.g., Technology).
- `industry`: Sub-industry (e.g., Software).
- `source`: Where the symbol was obtained from.
- `notes`: Any custom user notes.

## Symbol Format Rules
Symbols are automatically normalized:
- Converted to UPPERCASE.
- Leading and trailing spaces are removed.
- Cannot contain path traversal characters (e.g., `/`, `\`).
- Cannot exceed 15 characters.

## Duplicates & Invalid Symbols
- If a CSV contains duplicate symbols, the duplicates are skipped and a warning is generated.
- Invalid symbols (e.g., missing symbol, invalid characters) generate an error and are skipped. A validation report can be generated using the `universe-validate` command.

## Adding Your Own Symbols
You can replace the contents of `data/universe/watchlist.csv` with your own list, so long as it adheres to the required CSV structure.
