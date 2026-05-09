# Incident System Limitations

- **Heuristic Classification:** The incident classifier uses keyword heuristics. It may miss certain obscure failures or misclassify warnings as errors.
- **No Automatic Fixes:** A recovery plan is a list of *recommended* actions. It is not an AI agent that automatically resolves complex logic bugs.
- **Rollback is Dry-Run Default:** `rollback-execute` is disabled by default. If executed, it will still refuse to overwrite protected paths (like source code). It is primarily designed to safely restore data caches, models, and baseline fixtures.
- **No Cloud/External Backups:** All backups and incident logs are stored entirely locally on disk. If the local disk fails, the incident data is lost.
- **No Broker Telemetry:** The incident system has zero awareness of real broker connections or live trading portfolios because the system strictly forbids broker connections.
- **Not Investment Advice:** Incident and recovery reports refer only to the software's internal operation. "PASS" statuses indicate software stability, not a guarantee of trading profitability.
