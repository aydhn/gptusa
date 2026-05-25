# YFinance and Local CSV Adapters

**yfinance**: Implements the base wrapper for Yahoo Finance, but defaults to `allow_network=False`.
Any real fetch must be manually allowed through configuration in the future.

**local CSV**: A file-based fixture wrapper for reading datasets locally.
Path traversal guard is applied automatically. No writing capabilities.
