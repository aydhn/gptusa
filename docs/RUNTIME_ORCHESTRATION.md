# Runtime Orchestration

## Purpose
The Runtime Orchestration layer coordinates the execution of Market Scans locally. It strings together all previously built pipeline steps in a deterministic, safe sequence.

## Pipeline Steps
- **preflight**: Validates config, check directories
- **universe resolve**: Selects target symbols
- **data refresh**: Re-downloads data if configured
- **data readiness**: Confirms cache integrity
- **feature pipeline**: Generates composite features
- **strategy run**: Runs rule strategies
- **scoring/ranking/selection**: Narrows candidate list
- **risk evaluation/portfolio construction**: Allocates simulated portfolio
- **scan report**: Generates JSON output

## Mechanisms
- **Lock Manager**: Ensures no concurrent overlapping scans are executed.
- **Safe Stop**: Allows operators to gracefully halt the pipeline mid-run without destroying files.
- **Runtime Events**: All steps emit JSONL event logs.

## Important Note
This system explicitly avoids daemon or OS cron installations in this phase, preserving the purely local script execution model.
