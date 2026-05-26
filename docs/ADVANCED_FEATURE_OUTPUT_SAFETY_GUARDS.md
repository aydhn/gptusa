# Advanced Feature Output Safety Guards

Phase 118 enforces strict non-execution boundaries:
- `produces_trade_signal=False`
- `produces_order_decision=False`
- `produces_portfolio_weights=False`
- `activation_allowed=False`
- `active_paper_enabled=False`
- `network_used=False`
- `broker_used=False`

## Language Guards
All generated texts and metadata reports are scanned for forbidden execution language such as "emir gönderildi", "kesin al", "garanti kâr", "live order". Detection triggers an `AdvancedFeatureOutputSafetyValidationError` and blocks the generation of the review report.
