# Phase 145: ML Governance Closure and Explainability

This module implements Phase 145 of the USA Signal Bot project.

## Scope
- Ingest Phase 144 Drift Monitoring Outputs
- Generate Feature Attribution Proxies
- Generate Factor Contribution Summaries
- Generate Model, Regime, Calibration and Ensemble Explanations
- Produce Explainability Reports
- Enforce Advanced ML Final Audits
- Create Artifact Lineages
- Ensure strict Non-Activation Boundary

## Principles
1. Metadata Only - Outputs are research reports, not execution instructions.
2. No ML dependencies - Computation relies on pandas and stdlib instead of SHAP/LIME or heavy models.
3. Strict Safety Guards - Enforces boundaries against live deployment, trade signal generation, execution language, and active paper mutation.
