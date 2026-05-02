# Divergence Detection System

Phase 19 introduces the foundational architecture for Price/Oscillator Divergence Detection in the USA Signal Bot.

## Purpose
Divergence detection aims to identify instances where the price of an asset moves in the opposite direction of a technical oscillator (like RSI, MACD, ROC). These instances often hint at a weakening trend or a potential continuation of an existing trend.

**Important Note:** The output of this system is purely **Feature Data**, not trading signals. Divergences must be combined with market structure, regime analysis, or specific strategies before making trading decisions. This phase does not include backtesting or signal execution.

## Divergence Types

The system detects four primary types of divergences:

1.  **Regular Bullish Divergence:**
    *   **Condition:** Price makes a Lower Low (LL), but the Oscillator makes a Higher Low (HL).
    *   **Implication:** Downward momentum is waning; potential bullish reversal.
    *   **Code:** `1`

2.  **Regular Bearish Divergence:**
    *   **Condition:** Price makes a Higher High (HH), but the Oscillator makes a Lower High (LH).
    *   **Implication:** Upward momentum is waning; potential bearish reversal.
    *   **Code:** `-1`

3.  **Hidden Bullish Divergence:**
    *   **Condition:** Price makes a Higher Low (HL), but the Oscillator makes a Lower Low (LL).
    *   **Implication:** Indicates underlying strength; potential bullish trend continuation.
    *   **Code:** `2`

4.  **Hidden Bearish Divergence:**
    *   **Condition:** Price makes a Lower High (LH), but the Oscillator makes a Higher High (HH).
    *   **Implication:** Indicates underlying weakness; potential bearish trend continuation.
    *   **Code:** `-2`

## Detection Mechanism (Pivots)

Divergence detection relies on identifying "Swing Points" or "Pivots" on both the price series and the oscillator series, and then aligning them.

### Confirmation Modes

1.  **Confirmed Pivot (`confirmed_pivot`)** [Default]
    *   Requires a set number of bars on the *left* and the *right* to confirm a pivot.
    *   **Pros:** Highly accurate and filters out noise.
    *   **Cons (Future Leakage):** Because it requires `right_window` bars to form *after* the pivot, it inherently looks into the future. **If used blindly in a backtest, this will cause data leakage.** The feature is recorded at the pivot index, but in reality, it would only be known `right_window` bars later.
    *   **Usage:** Excellent for historical feature analysis, visualization, and training sets (if properly aligned). For live trading, you must delay the signal by `right_window` bars.

2.  **Left-Only Pivot (`left_only_pivot`)**
    *   Requires a set number of bars only on the *left* (rolling extreme).
    *   **Pros:** Zero look-ahead bias. Safe for real-time and strict backtesting.
    *   **Cons:** Very noisy. It identifies many "false" pivots that are quickly broken.

## CLI Usage

List available divergence indicators:
```bash
python -m usa_signal_bot divergence-indicator-list
```

View information about a divergence indicator set:
```bash
python -m usa_signal_bot divergence-indicator-set-info --set full_divergence
```
