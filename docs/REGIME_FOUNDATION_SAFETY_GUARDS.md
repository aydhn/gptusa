# Regime Foundation Safety Guards

To protect against inadvertent activation, the Regime Foundation incorporates safety validators.

## Guards Included:
- **No execution language:** Text parsing blocks commands like "kesin al", "garanti kâr", "buy", "sell".
- **Forbidden columns:** Dataset definitions block "buy_signal", "allocation", "portfolio_weight", etc.
- **No Side Effects:** Blocks network fetch, scraping, HTML parse, and Paid APIs.
- **No Data Leaks:** Prevents inclusion of `api_key` or `broker_order_id`.
- **Enforced Context Properties:** Hardcodes execution enablers (`active_paper_enabled`, `strategy_activation_allowed`) to `False`.
