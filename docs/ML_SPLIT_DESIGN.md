# ML Split Design

Defines how data is segmented into TRAIN, VALIDATION, and TEST sets.

- Time Series Holdout
- Walk-Forward Split
- Symbol-Aware Time Split
- Uses Embargo and Purge logic to mitigate leakage.
- No random shuffling to maintain time series integrity.
