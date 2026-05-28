# Final Closure Safety Guards

Phase 125 enforces rigorous safety guards to ensure the feature/factor engine produces pure research data, free of any execution logic or investment advice.

## Forbidden Elements
- **Trade Signals / Execution Language:** e.g., "buy", "sell", "order", "entry", "exit".
- **Absolute Financial Claims:** e.g., "garanti kâr", "kesin al".
- **Broker / Paper Mutation:** e.g., "broker", "live_order", "portfolio_weight".
- **Network / Deployment:** e.g., "deploy", "production_patch".

The final schema and safety validators explicitly scan artifacts and inputs to block these elements.
