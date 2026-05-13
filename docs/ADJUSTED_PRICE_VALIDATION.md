# Adjusted Price Validation

**DISCLAIMER: NOT INVESTMENT ADVICE. NO BROKER/LIVE EXECUTION.**
Ensures consistency between `close` and `adj_close` data columns. Significant jumps in the adjustment ratio trigger warnings or flag inconsistencies to prevent corrupted indicator behavior.

## Usage
`python -m usa_signal_bot adjusted-price-validate --symbol SPY`
