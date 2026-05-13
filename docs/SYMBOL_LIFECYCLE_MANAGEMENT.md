# Symbol Lifecycle Management

## Overview
Symbols (tickers) in the US market change frequently due to acquisitions, bankruptcies, ticker renames, or share class changes. Tracking these lifecycle events is essential for reliable backtesting and signal generation.

The **Symbol Lifecycle Management** layer provides a lightweight, local registry system to track symbol states over time.

## Symbol Lifecycle Statuses
Symbols can transition through several states:
- `ACTIVE`: Currently trading.
- `INACTIVE`: Technically still listed, but not trading actively.
- `DELISTED`: Removed from the exchange.
- `SUSPENDED`: Temporarily halted.
- `MERGED` / `ACQUIRED`: Absorbed by another entity.
- `SYMBOL_CHANGED`: Transitioned to a new ticker alias.
- `UNKNOWN`: Missing from registry.

## Local Registry & Aliases
Because this project strictly forbids paid external data APIs and web scraping, lifecycle tracking relies on a **Manual Lifecycle Registry** (`config/universe/symbol_lifecycle_registry.example.json`) and an **Alias Registry** (`config/universe/symbol_aliases.example.json`).

These JSON files can be manually maintained by the operator or partially inferred through historical snapshots (`infer_from_history`).

## Aliasing and Resolution
The `SymbolStatusResolver` attempts to trace a symbol through ticker changes to identify its predecessor or successor. Cyclical alias definitions will trigger warnings during lifecycle validation.

## CLI Usage
View basic lifecycle config info:
```bash
python -m usa_signal_bot universe-lifecycle-info
```
Generate example registry configurations:
```bash
python -m usa_signal_bot universe-lifecycle-write-examples
```
Query status for a specific symbol:
```bash
python -m usa_signal_bot symbol-status --symbol SPY
```

## Limitations
The manual registry is **not a guarantee** of official historical data accuracy. It operates purely as an operational guard.
