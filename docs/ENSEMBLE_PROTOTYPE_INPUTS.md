# Ensemble Prototype Inputs

Inputs for the offline ensemble evaluation layer:
- **Ensemble Preparation Reports:** Offline artifacts providing ensemble context.
- **Candidate Groups:** Registered candidate model definitions.
- **Blend Plans:** Blending coefficients designed in Phase 142.
- **Offline Prediction Artifacts:** Previous offline predictions from baseline candidate models.
- **Prediction Frame & Target Matrices:** Offline research CSV datasets for label/target correlation.

**Rules:**
- All inputs are read-only.
- Inputs must not contain execution paths, broker mappings, or live deployment parameters.
