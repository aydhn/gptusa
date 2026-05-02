# Feature Pipeline

The Feature Pipeline orchestrates the flow of data from the initial universe configuration, through the market data cache, and finally into the composite feature engine. It's designed to be robust, deterministic, and highly decoupled from external API limits (by relying strictly on local cache).

## Architecture Flow
The pipeline follows a distinct sequence of operations:

1. **Symbol Resolution**:
   - The pipeline first determines which symbols to process. If explicit symbols are provided via CLI arguments, it uses those.
   - If no explicit symbols are given, it defaults to reading the "eligible symbols" list from the most recent Universe Readiness Gate output.
   - As a final fallback, it may read directly from the active universe definition.

2. **Cache Validation**:
   - Before attempting any computations, the pipeline checks the local market data cache.
   - It verifies that complete data exists for all required symbols and timeframes.
   - Any missing symbols are flagged and removed from the active processing batch. The pipeline **does not** automatically initiate a data download—it strictly operates on the existing cache to avoid surprise network calls and API rate limiting.

3. **Composite Feature Computation**:
   - The verified cache data is passed to the `CompositeFeatureEngine`.
   - The engine computes the requested `CompositeFeatureSet` (e.g., core, technical, full).
   - If a specific feature group fails (e.g., an error calculating divergence), the engine can still return a `PARTIAL_SUCCESS` status, allowing the successful groups to be saved.

4. **Output Generation & Storage**:
   - The resulting features are stored in the local `features/` directory.
   - Partitioning strategies dictate how files are organized:
     - `by_group`: (Default) Separate JSONL files for trend, momentum, etc.
     - `combined`: A single merged output file.
     - `by_symbol` or `by_timeframe`: Available for alternative downstream consumption.

5. **Metadata and Reporting**:
   - The pipeline generates a comprehensive JSON report containing:
     - The exact composite set used.
     - The list of successfully processed symbols.
     - A list of symbols that were skipped due to missing cache data.
     - The output storage paths.

## CLI Usage

**Run the Full Feature Pipeline:**
```bash
python -m usa_signal_bot feature-pipeline-run --set core --timeframes 1d,1h --use-latest-eligible --max-symbols 50
```

**View the Storage Summary:**
```bash
python -m usa_signal_bot composite-feature-summary
```

## Important Considerations
- **No Data Fetching**: The feature pipeline strictly operates offline using cached OHLCV data. If you see warnings about missing cache symbols, you must run the data download pipeline first.
- **Fail-Safes**: The pipeline is designed to gracefully handle failures in individual feature groups without crashing the entire run. Always check the final metadata report for `PARTIAL_SUCCESS` statuses.
