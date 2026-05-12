# Data Provider Abstraction

This project uses a modular provider abstraction to safely fetch, cache, and manage historical stock data locally.

## Provider Types
* **YFinance**: Online free library (uses the `yfinance` module) for OHLCV, splits, and dividend data.
* **Local Cache**: Fetches previously saved responses from disk.
* **Local Fixture**: Supplies deterministic historical snippets for regression tests.
* **Manual File**: Ingests user-provided `.csv` or `.jsonl` files.

## Principles
* No Paid Providers: No API keys or subscriptions required.
* No HTML Scraping: We don't scrape dashboards or websites using Selenium/Playwright.
* Capability Checks: Routing only directs requests to providers claiming to support the required features.

## CLI Usage
Check provider capability profiles:
`python -m usa_signal_bot provider-capabilities`

Fetch a symbol:
`python -m usa_signal_bot provider-fetch-test --symbol SPY --offline`
