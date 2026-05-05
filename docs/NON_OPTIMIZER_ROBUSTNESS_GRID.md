# Non-Optimizer Robustness Grid

In traditional backtesting platforms, a "parameter grid search" is often used to optimize the strategy. This system strictly prohibits that paradigm. We implement a **Non-Optimizer Robustness Grid**.

## Robustness vs. Overfitting
Optimizers search for the highest peak in performance. However, these peaks are often isolated outliers on a parameter landscape, leading to severe overfitting. When trading out-of-sample data, these isolated peaks tend to collapse.

Instead, we look for **plateaus of robustness**. A plateau is a region where varying parameters slightly does not cause a drastic drop in performance.

## Max Cell Guard
Because evaluating parameters creates a combinatorial explosion, we employ a **Max Cell Guard**.
- `max_cells` limits how many cells will be evaluated.
- `hard_max_cells` is the absolute limit set in the configuration.

If a generated grid exceeds these limits, the runner will either truncate the grid deterministically or throw a validation error.

## Avoidance of Best Parameters
The validation engines explicitly ensure that no resulting JSON payload contains fields like `best_params` or `optimal_return`. The goal is to provide a comprehensive heat-map-like text summary without giving actionable, direct trading advice.
