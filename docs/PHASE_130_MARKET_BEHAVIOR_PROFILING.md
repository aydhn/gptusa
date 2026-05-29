# Phase 130: Market Behavior Profiling

This phase represents the fifth layer in the Regime Classification engine. It digests the outputs from Phase 129 `RegimeTransitionFullReview` in a read-only manner.

## Objectives
- Perform market behavior profiling using local regime diagnostics artifacts.
- Produce behavior profiles and regime summaries without training models or executing prediction logic.
- Compile these elements into a purely informational Regime Diagnostics Report.
- Use behavior profiling to understand structural characteristics of market data as generated heuristically by Phase 128/129.

## Non-Activation Rules
Phase 130 is explicitly NOT an active paper trading, execution, strategy enablement, or deployment phase.
- **No Model Training**: Heavy ML tools like clustering, hmmlearn, etc are forbidden. Profiles are built heuristically.
- **No Model Prediction**: No classification tasks.
- **No Broker**: No interactions with broker APIs.
- **No Executions/Orders**: No order decisions or portfolio weight distributions are generated.

## CLI Access
You can interact with Phase 130 using:
```bash
python -m usa_signal_bot market-behavior-info
python -m usa_signal_bot build-market-behavior-profiles --write
python -m usa_signal_bot market-behavior-review --write
```
