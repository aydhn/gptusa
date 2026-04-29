# Market Data Downloads & Orchestration

The USA Signal Bot relies on a dedicated module (`MarketDataDownloader`) to manage network calls to external data providers (like `yfinance`), ensuring caching and batch execution are correctly respected.

## MarketDataRequest and Response Workflow
1. A user triggers a fetch request specifying symbols and timeframes.
2. The Request is intercepted by the selected `MarketDataProvider` and evaluated for compliance via provider guards.
3. The Provider creates a chunked fetch plan based on data source limit policies.
4. Downloader executes batches with optional delays to mitigate rate-limiting.
5. Responses are wrapped into `OHLCVBar` domain structures, evaluated for quality, cached incrementally, and summarized.

## Storage
- **Directory**: `data/cache/market_data/`
- **Format**: JSONL files, broken down iteratively by deterministic paths (symbol, timeframe, provider, start, end).
- **Summary**: Download operations generate a summary JSON summarizing fetch results.

## CLI Usage
View available providers:
```bash
python -m usa_signal_bot data-provider-info
```

Execute a standard symbol request:
```bash
python -m usa_signal_bot data-download --symbols AAPL,MSFT,SPY --timeframe 1d --start 2023-01-01 --end 2024-01-01
```

Download data derived from an entire defined universe:
```bash
python -m usa_signal_bot data-download-universe --timeframe 1d --limit 20
```

Inspect cache statistics:
```bash
python -m usa_signal_bot data-cache-info
```
