# Matrix Assembly

## Feature Matrix
Joins resolved sources on `symbol` and `timestamp`.
Does not perform model training, scaling, or selection in this step.

## Target Matrix
Computes research targets such as:
- Forward returns
- Forward volatility
- Forward drawdown
These do NOT represent trade signals or portfolio allocations.

## Label Matrix
Creates bucketized labels for ML experiments:
- `positive_return_bucket`, `negative_return_bucket`, `neutral_return_bucket`
- `high_volatility_bucket`, `medium_volatility_bucket`, `low_volatility_bucket`
- `shallow_drawdown_bucket`, `medium_drawdown_bucket`, `deep_drawdown_bucket`
