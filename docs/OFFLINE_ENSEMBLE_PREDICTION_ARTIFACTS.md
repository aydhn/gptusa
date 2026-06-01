# Offline Ensemble Prediction Artifacts

The artifacts generated are purely for ML evaluation:
- `research_ensemble_prediction_value`
- `research_ensemble_prediction_label`
- `research_ensemble_prediction_score`
- `research_ensemble_prediction_probability`
- `diagnostic_metadata`

**Prohibited Output Fields:**
Any columns implying trading actions or allocations are explicitly forbidden, such as: `buy`, `sell`, `entry`, `exit`, `order`, `broker_order`, `paper_order`, `live_order`, `position`, `portfolio_weight`, `target_weight`, `allocation`, `sent_to_broker`, `strategy_active`, `deployment_enabled`, `production_patch`.
Offline ensemble prediction is purely research data.
