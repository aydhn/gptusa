# Provider Quality Scoring

Data fetched from a provider is scored based on multiple dimensions:
- Freshness: Is the data up to date relative to the last trading session?
- Completeness: Does it have enough rows to be useful?
- Schema: Does the shape of the data match expectations?
- OHLCV Consistency: Are highs higher than lows? Are volumes non-negative?
- Latency: Did it respond quickly?
- Error Rate: Are there any explicit warnings or exceptions thrown?

## Usage
Score a local dummy test response:
`python -m usa_signal_bot provider-quality-test --write`
