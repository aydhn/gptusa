# Candidate Selection System

The Candidate Selection phase processes ranked signals, filtering out the noise to produce a focused shortlist (`SelectedCandidate`) suitable for deeper research.

## Purpose

To enforce risk logic, strategy limits, and symbol diversification, narrowing down a high volume of signals to an actionable daily watchlist.

## Selection Logic & Rejection Reasons

Signals are evaluated against strict thresholds. They may be rejected for the following reasons:
- **`LOW_RANK_SCORE`**: The ranked score falls below the required threshold (default `45.0`).
- **`LOW_CONFIDENCE`**: The rule strategy did not assign a high enough initial confidence.
- **`HIGH_RISK_FLAGS`**: The presence of severe risk warnings (e.g., `EXTREME_VOLATILITY`).
- **`SHORT Action Disabled`**: By default, `SHORT` actions are disabled (`allow_short_action = False`).
- **`TOO_MANY_PER_SYMBOL`**: A symbol exceeds the maximum number of selected candidates.
- **`TOO_MANY_PER_STRATEGY`**: A strategy exceeds its daily allocation of selected candidates.

Valid signals with a `WATCH` action are classified as `WATCHLISTED`, while `LONG` actions become `SELECTED`.

## Limits

Limits are configurable via `default.yaml`:
*   `max_candidates`: Global limit for the system per run (default: 20).
*   `max_candidates_per_symbol`: Prevent overexposure to a single ticker.
*   `max_candidates_per_strategy`: Avoid a single strategy spamming the candidate list.

**Important Note**: A Selected Candidate represents an opportunity designated for research, paper trading, or backtesting. **It is not an active trade order.**

## CLI Usage Examples

Select candidates from an existing JSONL file:
```bash
python -m usa_signal_bot signal-select-candidates --file data/signals/example.jsonl --max-candidates 10 --write
```

View a summary of recently selected candidates:
```bash
python -m usa_signal_bot selected-candidates-summary
```
