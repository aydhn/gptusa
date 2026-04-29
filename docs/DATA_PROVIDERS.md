# Data Providers Foundation

USA Signal Bot uses a robust, interface-driven provider abstraction layer. This layer isolates strategy code from the actual mechanics of fetching data, ensuring compliance with strict project rules.

## The Provider Interface
`MarketDataProvider` is the abstract base class that defines the contract all market data adapters must fulfill. It requires defining:
- **Capability:** Feature flags about what the provider supports (daily vs intraday data, batch limits, etc.).
- **Policy:** Rules on retries, rate limits, and caching.
- **Methods:** Including `validate_request`, `build_fetch_plan`, `fetch_ohlcv`, and `check_status`.

## Guard Rails and Rules
The system enforces strict rules via centralized provider guards:
1. **Free Only:** Providers must be free to use.
2. **No Web Scraping:** Using BeautifulSoup/Selenium/Scrapy against web DOMs is completely forbidden to prevent fragility and API terms of service violations.
3. **No Broker Dependencies:** The provider layer explicitly bans broker backends (like Alpaca, Interactive Brokers, Robinhood) because this project operates in local paper trading mode only and separates order execution from historical data collection.

## Mock Provider
In Phase 7, no real data fetching is implemented. Instead, a `MockMarketDataProvider` is registered as the default. It validates requests, tests the interface, and returns deterministically generated, sahte (fake) data for testing.

## yfinance (Reserved)
The default fallback for real data in future phases is `yfinance`. However, in Phase 7, `yfinance` is only represented by a reserved capability profile. Actual downloads via `yfinance` will be built out in a subsequent adapter phase.
