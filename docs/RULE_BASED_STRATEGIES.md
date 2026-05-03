# Rule-Based Strategies

USA Signal Bot includes a robust rule-based strategy framework designed to generate signal candidates based on predefined, transparent conditions. These strategies are non-execution candidates meant for watchlists, confluence aggregation, or future integration into backtests.

## Architecture

- **RuleCondition:** Defines a single logical rule (e.g., `close_ema_20 > close_ema_50`), with thresholds, weights, and operators.
- **RuleStrategyDefinition:** Aggregates conditions into a coherent trading idea (e.g., Trend Following), specifying required features, minimal passed conditions, and a base score.
- **RuleEvaluation:** Results of applying a definition to feature data, resulting in a normalized score (0-100) and a `RuleSignalBias`.
- **Strategy Engine Integration:** Rule strategies act seamlessly as any other strategy in the registry but guarantee no broker routing.

## Usage

You can list all rule-based strategies:
```bash
python -m usa_signal_bot rule-strategy-list
```

Run a specific strategy using cached feature data:
```bash
python -m usa_signal_bot rule-strategy-run-feature-store --strategy trend_following_rule --symbols AAPL --timeframes 1d
```

## Watch-Only Default

By default, all rule strategies yield a `WATCH` action. They identify *candidates* and generate `INSUFFICIENT_FEATURES` or `CONFLICTING_FEATURES` risk flags if data is incomplete or unclear.
