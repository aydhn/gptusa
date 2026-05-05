# Market Scan Loop

## Foundation
The Market Scan loop allows for a single `MarketScanRequest` to trigger the entire USA Signal Bot pipeline end-to-end.

## Execution Scopes
- `explicit_symbols`
- `latest_eligible_universe`
- `active_universe`
- `small_test_set`

## Configuration
By default `refresh_data` is `False`. The scan generates outputs into `data/runtime/scans/<run_id>` but does NOT act on them externally.

*Crucially, the Market Scan Result does not constitute investment advice. No paper trades or live trades are issued.*
