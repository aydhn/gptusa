# Cross-Sectional Feature Engine

## Purpose
To evaluate symbols relative to their peers or a benchmark at exactly the same timestamp.

## Process
1. **Universe Definition**: A set of symbols (e.g., AAPL, MSFT, SPY) valid for comparison.
2. **Alignment**: Ensures that all symbols have matching timestamp rows. Discards misaligned data.
3. **Cross-Sectional Rank**: Computes the percentile rank of a feature (e.g., Momentum) across all symbols in the universe for a given day.
4. **Cross-Sectional Z-Score**: Normalizes a feature against the cross-sectional mean and standard deviation.
5. **Relative Strength**: Computes the difference or ratio of a symbol's feature compared to a benchmark (e.g., SPY).

**Disclaimer**: These rankings are research inputs only. A cross-sectional rank of 100% does NOT mean "Buy", and 0% does NOT mean "Sell". Portfolio construction is explicitly forbidden in Phase 118.
