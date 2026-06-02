# DRIFT_MONITORING_INPUTS

## Inputs
Phase 144 ingest the following artifacts from Phase 143:
- **Non-Activation Ensemble Registry:** The registry containing the ensemble models.
- **Offline Ensemble Evaluation Reports:** The performance reports of the ensemble.
- **Offline Ensemble Prediction Artifacts:** The static predictions made by the ensemble on historical splits.
- **Feature, Label, and Regime Matrices:** Reference and monitoring datasets for drift calculation.

## Constraints
All inputs are ingested in a strictly read-only mode. The system enforces validation to ensure no live broker connections, deployment flags, or network fetching attempts are embedded in the inputs.
