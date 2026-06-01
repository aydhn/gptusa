# Post-Training Validation

Validates output integrity and constraints after candidate evaluation.

## Rules Validated
- Model registry consistency.
- Candidate shortlist consistency.
- Offline predictions availability.
- Probability/score output validity.
- True labels availability.
- Split assignment consistency.
- **Safety checks:**
  - No forbidden outputs.
  - No live inference.
  - No calibration fitting.
  - No deployment.
