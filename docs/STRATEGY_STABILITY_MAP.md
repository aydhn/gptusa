# Strategy Stability Map

The Strategy Stability Map processes the results of a sensitivity run to classify different regions of the parameter landscape.

## Local Neighborhood Stability
For any given cell, the system identifies its "neighbors" (cells with at most 1 parameter difference). By calculating the coefficient of variation (CV) for the primary metric among these neighbors, a `local_stability_score` (0-100) is generated.

## Regions
- **ROBUST_REGION:** Cells that perform above the global median and possess a high local stability score.
- **FRAGILE_REGION:** Cells that may perform well but have a very low local stability score (suggesting an isolated spike).
- **NEUTRAL_REGION:** Average performance with average stability.
- **OUTLIER_REGION:** Extreme high performance but dangerously low stability.
- **INSUFFICIENT_DATA:** Cells without enough completed neighbors to accurately assess stability.

## CLI Usage
To view the stability map of the most recent sensitivity run:
`python -m usa_signal_bot stability-map --latest`
