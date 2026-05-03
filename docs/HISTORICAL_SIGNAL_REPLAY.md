# Historical Signal Replay

Historical Signal Replay is a fundamental component of the backtesting engine in USA Signal Bot. It allows you to simulate the execution of your generated signals over cached historical market data to gauge theoretical past performance.

## Overview
Unlike live execution, signal replay operates entirely on files:
1. It reads pre-generated signals from JSONL files (`StrategySignal` or `SelectedCandidate`).
2. It parses cached market data (`OHLCVBar`) spanning the same timestamps.
3. It reconstructs the market timeline deterministically to determine if and when signals would have executed.

## Signal Modes
* `WATCH_AS_LONG_CANDIDATE`: Converts "WATCH" signals into potential "LONG" execution candidates for theoretical entry timing analysis.
* `LONG_ONLY`: Restricts entries purely to "LONG" signals.
* `WATCH_ONLY_NO_TRADES`: Replays events to verify system integrity but generates no actual trades or order intents.
* `SIGNAL_ACTION_BASED`: Uses the direct mapping of signal actions (LONG, SHORT) where applicable.

## Same-Bar Fill Prevention
To mitigate look-ahead bias, if a signal is generated based on the close of Bar $T_0$, it cannot be filled at the close of Bar $T_0$. The default order logic uses `NEXT_OPEN`, ensuring execution at the open of Bar $T_1$.

## Usage Example
Run a backtest using pre-selected candidates from the ranking phase:
```bash
python -m usa_signal_bot backtest-run-candidates --candidates-file data/signals/ranking/selected_candidates.jsonl --timeframe 1d --write
```
