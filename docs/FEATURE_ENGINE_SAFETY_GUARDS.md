# Feature Engine Safety Guards

To guarantee non-execution, the Phase 116 foundation uses `feature_safety_validator.py`.

Safety guards ensure:
- `produces_trade_signal = false`
- `activation_allowed = false`
- `broker_execution_enabled = false`
- No "kesin al", "strong buy", or similar Turkish/English execution terminology exists in descriptions.
- `network_default_enabled = false`
- `paid_api_used = false`

A breach of these guards causes the context to fail immediately and report a `FeatureFoundationRiskFlag`.
