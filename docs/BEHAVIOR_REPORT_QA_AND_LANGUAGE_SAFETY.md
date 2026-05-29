# Behavior Report QA and Language Safety

Phase 130 introduces a strict Report QA step to scan generated text for forbidden language.

## Forbidden Language Rules
- **Investment Advice Language**: "kesin al", "garanti kâr", "risksiz kazanç".
- **Trade Signal Language**: "buy signal", "sell signal", "strong buy".
- **Order Decision Language**: "entry", "exit", "broker order".
- **Portfolio Allocation Language**: "portfolio weight", "target weight", "allocation".
- **Guarantee Language**: "guaranteed", "no risk".
- **Broker Execution Language**: "sent to broker", "executed".
- **Deployment Language**: "deploy", "production patch".
- **Secret Language**: "api_key", "password".

Failure to pass QA will **block** the Readiness Gate and prevent readiness for Phase 131.
