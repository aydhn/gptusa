# Dry Admission Dossier Limitations

As part of the strict non-execution local boundary policy, the Dry Admission Dossier system holds the following absolute limitations:
1. **Local Metadata Only:** The dossier does not push configs to external repos, cloud storage, or active databases. It is a local JSON/JSONL store only.
2. **Not An Approval:** The Dry-Admission Acceptance Seal is strictly an internal checksum of completed safety checks. It is NOT an active paper, live, demo, or rehearsal execution approval.
3. **No True Rehearsal Runtime:** The Rehearsal Blocker acts purely to simulate attempts and ensure they return as BLOCKED. It does not spin up a live or local trade rehearsal.
4. **No Broker Integration:** Absolutely no code touches Broker APIs (Alpaca, IBKR, etc.).
5. **No Paper Mutation:** The process operates on read-only snapshots and never writes to `paper_store`.
6. **No Orders/Fills:** It does not create, simulate, or mock actual fills or orders during the dossier process.
7. **No Real Notifications:** Uses localized print statements or local logs. No real messages are dispatched via Telegram.
8. **No Investment Advice:** All metrics, evaluations, and acceptances are strictly mechanical workflow guards and explicitly disclaim any guarantee of profitability.
