# Paper Runtime Integration

This document outlines the integration of the local paper trading engine into the runtime scan pipeline.

## Overview
The paper runtime translates `RiskDecision`, `AllocationResult`, `SelectedCandidate`, or `StrategySignal` objects into `PaperOrderIntent`s, which are then processed by the `PaperTradingEngine`. The engine simulates order validation, acceptance, queueing, and fills locally without broker execution.

## Pipeline Integration
During a `MarketScanOrchestrator` execution, the `PAPER_TRADING` step can be optionally activated (default: disabled) via `--paper`. When enabled, it pulls the output file paths from the current scan context (e.g., allocations or risk decisions) to drive the local paper simulation.

## Execution Modes
- **dry_run**: The engine validates orders but forces a skipped status simulating no fills.
- **validate_only**: Validates intents and rejects them if they fail, but doesn't transition them to queue/fill stages.
- **local_simulated**: Simulates execution by resolving the price from local historical data caches.

## Examples
Run a full scan with paper simulation:
```bash
python -m usa_signal_bot scan-run-once --scope small_test_set --paper --paper-execution-mode local_simulated --paper-starting-cash 100000.0
```

Run paper engine manually against existing risk decisions:
```bash
python -m usa_signal_bot paper-runtime-run --source risk_decisions --risk-decisions-file data/runtime/scans/scan_xyz/risk_decisions.jsonl --execution-mode local_simulated
```

## Disclaimers
This simulation does **not** generate broker or live orders. It is designed entirely as a historical/test simulation layer built strictly on local cache. The paper execution and logic constitute NO INVESTMENT ADVICE.
