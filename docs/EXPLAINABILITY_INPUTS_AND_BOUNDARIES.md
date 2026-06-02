# Explainability Inputs and Boundaries

In Phase 145, inputs to the explainability and governance pipelines are strictly read-only references to prior phase outputs:

- Monitoring packages
- Drift metrics
- Ensemble evaluation reports
- Model cards
- Phase reviews
- Feature/factor matrices

These inputs have strictly no broker, live, paper, or deployment connection. Their outputs are exclusively metadata, designed to satisfy the governance closure without crossing the execution boundary.
