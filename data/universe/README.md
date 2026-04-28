# USA Universe Files

This directory contains seed files for the USA Signal Bot universe.
These files are **NOT** the full USA universe. They are sample files intended for bootstrapping, testing, and demonstrating functionality.

## Files

- `watchlist.csv`: A default, mixed list of high liquidity ETFs and Stocks to provide a basic starting point.
- `sample_stocks.csv`: A small sample file containing exclusively stocks.
- `sample_etfs.csv`: A small sample file containing exclusively ETFs.

## CSV Column Standard

To add your own symbols, use a CSV file with at least the required columns.

**Required columns:**
- `symbol`
- `asset_type` (stock or etf)

**Optional columns:**
- `name`
- `exchange`
- `currency` (defaults to USD)
- `active` (defaults to true)
- `sector`
- `industry`
- `source`
- `notes`

Future phases will provide automated integrations and a mechanism for pulling a broader universe list.
