# Strategy Families

The rule-based strategy pack comprises several families, each focusing on a distinct market characteristic.

### 1. Trend Following
- **Strategy:** `trend_following_rule`
- **Features:** EMA alignments, slopes, price distance to moving averages, and basic trend strength.
- **Goal:** Identify strong, established directional moves.

### 2. Momentum
- **Strategy:** `momentum_continuation_rule`
- **Features:** RSI, Rate of Change (ROC), and Momentum oscillators.
- **Goal:** Confirm the acceleration and continuation of an existing move.

### 3. Mean Reversion
- **Strategy:** `mean_reversion_rule`
- **Features:** Bollinger %B extremes, RSI extremes, stretched distance from SMA.
- **Goal:** Identify exhausted moves likely to snap back to the mean.

### 4. Volatility Breakout
- **Strategy:** `volatility_breakout_rule`
- **Features:** Breakout distance, volatility compression, and Normalized ATR.
- **Goal:** Detect explosive moves out of consolidation periods.

### 5. Volume Confirmation
- **Strategy:** `volume_confirmation_rule`
- **Features:** Relative volume, dollar volume, volume trend strength.
- **Goal:** Confirm that institutional/heavy volume is supporting the price action.

### 6. Composite Technical
- **Strategy:** `composite_technical_rule`
- **Goal:** Combines aspects from all families above into a multi-factor score.
