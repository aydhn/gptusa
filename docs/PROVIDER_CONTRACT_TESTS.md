# Provider Contract Tests

Data providers are verified locally through a contract test runner without internet connections.

Tested areas:
1. Valid adapter spec payload.
2. No forbidden methods (`live_order`, `scrape`, etc.).
3. `metadata_only` execution fallback.
4. No network fetch by default.
5. Correct OHLCV schema normalization.
