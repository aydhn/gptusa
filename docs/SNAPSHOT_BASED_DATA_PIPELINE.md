# Snapshot-Based Data Pipeline

## Why Snapshot-Based?
As the universe expands to thousands of symbols, attempting to download data "on the fly" without a locked reference point leads to inconsistent datasets. By tying the pipeline to a specific snapshot, we ensure reproducibility. If a run fails halfway, we know exactly what the expected universe was.

## The Pipeline Flow
1. **Universe Resolution**: The Active Universe Resolver locks in the target symbols.
2. **Multi-Timeframe Request**: The system builds a refresh plan across all required timeframes (e.g., `1d`, `1h`, `15m`).
3. **Cache or Refresh**: Symbols are evaluated against cache TTLs.
4. **Validation & Repair**: Downloaded data is validated and anomalous bars are dropped/repaired.
5. **Coverage & Readiness**: Coverage density is measured, and Data Readiness scores are calculated per symbol.
6. **Readiness Gate**: The Universe Readiness Gate evaluates the reports and approves/rejects symbols.

## Large Universes and Batching
To handle massive universes, the pipeline utilizes a `--limit` and `batch_size`. The `SymbolBatch` system provides rough runtime estimates and ensures memory limits aren't exceeded by writing data atomically as it progresses.

## Run Metadata
Each execution generates a `UniverseDataRun` record stored in `data/universe/runs/`. This JSON file tracks the success/failure of each pipeline step (`RESOLVE_UNIVERSE`, `DOWNLOAD_DATA`, `READINESS_GATE`, etc.).

## Output Files
At the end of a successful run, the following files are produced in the run directory:
- `run_metadata.json`
- `active_resolution.json`
- `coverage_report.json`
- `readiness_report.json`
- `gate_report.json`

## CLI Examples

Plan a multi-timeframe download for the active universe:
```bash
python -m usa_signal_bot active-universe-plan --timeframes 1d,1h --limit 50
```

Execute the download pipeline:
```bash
python -m usa_signal_bot active-universe-download --timeframes 1d,1h --limit 50
```
