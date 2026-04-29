# Data Repair Pipeline

## Repair Philosophy
Data repair aims to maximize usable data by addressing minor flaws without introducing false information. If a bar is structurally illogical and cannot be reliably corrected, the safest approach is to drop the bar entirely rather than synthesize prices. Repair actions are never silent; they must be logged and audited.

## Bar Dropping Rules
A bar is dropped if:
- Prices are zero or negative.
- High is less than low.
- Volume is negative.
- The symbol or timestamp is missing.

## Warning Triggers (Bars Kept)
A bar is kept but flagged with a warning if:
- Volume is exactly zero (unless explicitly forbidden in config).
- It breaks monotonic chronological sequence (it will be sorted instead of dropped).

## Handling Missing Volume
If volume is `None` or absent, the pipeline can safely assume `0.0` (indicating no observed volume rather than negative/corrupt volume). This is configurable via `fill_missing_volume_with_zero`.

## Duplicate Bars
If exact duplicates exist (same symbol, timeframe, timestamp), the repair pipeline retains the first encountered valid bar and drops subsequent duplicates to prevent counting the same volume or price action multiple times.

## Repair Reports & Auditing
Every repair action is cataloged in a `DataRepairReport` consisting of original counts, dropped counts, and a list of specific `DataRepairAction` items detailing the reason for each change. Repair is never silent.

## Overwriting and Backups
When manually running the cache repair CLI, overwriting the original file is disabled by default. If `--overwrite` is specified, the system will create a `.bak` backup file alongside the original cache file before applying atomic writes to prevent data loss.
