# Factor Composition Safety Guards

Phase 120 implements the `factor_composition_safety_validator.py` and `factor_composition_validation.py` modules to strictly enforce project non-execution policies.

## Validation Targets
- **Execution State Flags**: Any `produces_trade_signal`, `produces_order_decision`, `produces_portfolio_weights` = True is a block.
- **Language Detection**: Descriptions, payloads, and strings are checked against words like "buy", "sell", "kesin kâr", "emir gönderildi", "sent_to_broker".
- **Column Detection**: Input/Output columns cannot contain execution-related keywords (except `macd_signal` inherited via safe technical indicators).
- **Network / Mutation Guards**: Validates payload fields to ensure `network_used`, `broker_used`, `scraping_used`, etc. are all explicitly `False`.

Any failure results in a `FactorCompositionValidationError` preventing report generation.
