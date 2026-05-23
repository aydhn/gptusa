# Final Paper Sandbox Bridge

The Final Paper Sandbox Bridge is a no-write metadata bridge, NOT a real paper runtime. It defines routing permissions to ensure strict isolation.

## Route Map
- Read-only allowed: READ_MARKET_DATA, READ_SIGNAL_PREVIEW, READ_RISK_PREVIEW, READ_PAPER_SNAPSHOT.
- Denied: WRITE_PAPER_STATE, CREATE_PAPER_ORDER, UPDATE_POSITION, UPDATE_PORTFOLIO, PATCH_CONFIG, ENABLE_ACTIVE_PAPER, SEND_BROKER_ORDER, SEND_TELEGRAM_REAL.

## CLI Commands
- `python -m usa_signal_bot sandbox-bridge-routes --write`
- `python -m usa_signal_bot sandbox-bridge-envelope --write`
- `python -m usa_signal_bot sandbox-bridge-route-guard --write`
