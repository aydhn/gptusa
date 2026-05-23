# Admission Review Limitations

This document lists the strict, non-negotiable limitations of the Guarded Paper Mode Admission Review process in Phase 87.

## Functional Limitations
1. **Metadata Only:** The entire admission review process produces only JSON/JSONL metadata reports.
2. **Not Activation:** Ledger reconciliation, admission decision, and final transition checkpoints are NOT authorizations for live trading or active paper mode.
3. **No Broker API:** There is absolutely no code to connect to live or demo broker APIs.
4. **No Paper Mutation:** The existing paper runtime is accessed via a read-only snapshot adapter. Zero writes are permitted.
5. **No Telegram Real Send:** All notifications are generated as dry-run strings or objects; no real network requests are made.
6. **Not Investment Advice:** All decisions, risk flags, and evaluations are for local engineering and compliance purposes only.
