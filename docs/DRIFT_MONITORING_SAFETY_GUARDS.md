# DRIFT_MONITORING_SAFETY_GUARDS

## Enforced Boundaries
To prevent accidental live trading or deployment, Phase 144 enforces the following rules via the `NonActivationDriftBoundary`:
1. **Offline Only:** All drift baseline calculations must use offline, historical data.
2. **Metadata Only:** The monitoring package is restricted to generating metadata and artifacts.
3. **No Execution:** The system is explicitly blocked from issuing broker orders, updating paper trading state, or sending real Telegram messages.
4. **No Unsafe Language:** Output artifacts are scanned to block phrases like "buy", "sell", "guaranteed profit", "portfolio weight", or "target allocation".
5. **No Network:** The module is prohibited from scraping the web, parsing HTML, or fetching data from paid APIs during execution.
