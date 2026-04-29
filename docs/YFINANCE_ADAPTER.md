# yfinance Adapter

The `yfinance` adapter acts as the first genuine, free data provider implemented for USA Signal Bot (Phase 8).

## Purpose
It uses the free Yahoo Finance library `yfinance` to fetch OHLCV (Open, High, Low, Close, Volume) data without requiring paid API keys, violating the scraping policy directly in-project, or engaging in live broker order routing.

## Details
- **Free:** No API keys are required.
- **Provider Guards:** Respects strict configuration prohibiting the integration of paid providers or live-trading broker APIs.
- **Limits:** Yahoo Finance may impose its own rate limits or intraday caps. A batching mechanism has been applied to respect sensible request frequencies.
- **Auto Adjust:** Controlled via project configuration or command-line overrides, allowing the differentiation between `Close` and `Adj Close`.

## Supported Timeframes
It safely parses internal standard timeframes into Yahoo's expected syntax:
- `1d`, `1wk`, `1h`, `30m`, `15m`, `5m`, `1m`
