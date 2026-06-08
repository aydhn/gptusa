# Equal and Sizing-Score Sandbox Allocations

## Implementation Details
1. **Equal Sandbox Allocation:** Evenly spreads out allocation fractions to active eligible items (weight = 1/N).
2. **Sizing Score Allocation:** Processes sizing weights generated in prior cycles and computes specific proportional sandbox targets (weight = Score / Total Score).

## Safety Restraints
Both techniques populate `normalized_sandbox_weight`. Under absolutely no circumstances will they yield realistic order or capital deployment instructions. The intent remains explicitly analytical, preventing investment guidance output.
