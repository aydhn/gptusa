# Rolling Windows in Walk-Forward Analysis

Rolling windows dictate how historical data is partitioned into Training (In-Sample) and Testing (Out-Of-Sample) periods.

## Key Parameters
- `train_window_days`: The length of the In-Sample period.
- `test_window_days`: The length of the Out-Of-Sample period immediately following the train window.
- `step_days`: The number of days the window shifts forward for the next iteration.
- `max_windows`: The maximum number of windows to generate.
- `include_partial_last_window`: Whether to include the final window if it does not cover the full `test_window_days`.

## Supported Modes
1. **Rolling**: The training window has a fixed length and rolls forward by `step_days`.
2. **Anchored**: The training window's start date is fixed, but its end date expands forward by `step_days`.
3. **Expanding**: Functionally similar to Anchored, starting with `min_train_days` and expanding forward.

## Example
To see how windows are generated without running a full backtest:
```bash
python -m usa_signal_bot walk-forward-plan --start 2021-01-01 --end 2025-01-01 --mode rolling --train-days 365 --test-days 90 --step-days 90
```
