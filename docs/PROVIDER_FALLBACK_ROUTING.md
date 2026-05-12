# Provider Fallback Routing

We employ a unified router that determines the correct provider based on configuration and quality scores.

## Cache-First Routing
If enabled, the router attempts the Local Cache first. If data is present, fresh, and complete, it is used immediately.

## Quality-Aware Fallback
If the active provider (e.g., YFinance) throws an error or returns data below the configured `min_quality_score`, the router falls back to alternative local sources, recording a `fallback_used` flag.

## Usage
Test the router with a fallback scenario offline:
`python -m usa_signal_bot provider-route-test --symbol SPY --offline --write`
