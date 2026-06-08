# Sizing Cap and Floor Rules

Cap and Floor rules guarantee that prototype fraction results strictly fall within:
- `max_prototype_fraction`
- `min_prototype_fraction`

## Rules Evaluation
The `apply_sizing_cap_floor_rules` logic limits raw fraction calculation outputs. These act purely as constraint validators for prototypes and are NOT limit orders or actual trade thresholds.
