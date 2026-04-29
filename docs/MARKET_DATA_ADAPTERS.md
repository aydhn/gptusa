# Market Data Adapters Architecture

The Market Data Adapter architecture sits behind the `MarketDataProvider` interface. It defines standard data request and response contracts.

## Key Models

- **MarketDataRequest:** Encapsulates what data is needed (`symbols`, `timeframe`, `start_date`, `end_date`, `provider_name`). It also includes flags for caching and adjusted data preferences.
- **MarketDataResponse:** Packages the returned data into standard `OHLCVBar` domain objects, along with operation metadata (success flags, cache usage, error messages).
- **ProviderFetchPlan:** Before making a fetch request, providers generate a fetch plan to detail how they will chunk/batch the requests and whether caching will be applied.
- **OHLCVBar:** The standardized, validated price structure returned by all providers.

## Implementation Flow
When a component requests data:
1. The request specifies the `provider_name`.
2. The `ProviderRegistry` looks up the corresponding initialized `MarketDataProvider`.
3. The provider verifies capability guards and parses the request into a `ProviderFetchPlan`.
4. (Phase 7 stops here, returning Mock data). In future phases, the provider delegates to its underlying adapter library (like `yfinance`) applying the defined Rate Limits, Retry Logic, and Caching before formatting to a standard `MarketDataResponse`.
