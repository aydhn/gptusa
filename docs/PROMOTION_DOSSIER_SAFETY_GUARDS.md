# Promotion Dossier Safety Guards

To guarantee zero-risk execution during promotion, the following guards are strictly enforced:

1. **No active paper enable:** `allowed_for_active_paper` validation.
2. **No paper state mutation:** Read-only snapshots prevent ledger changes.
3. **No paper order:** Broker/Paper endpoints blocked.
4. **No broker order:** Validations catch fields like `broker_order_id`.
5. **No Telegram real send:** Dry-run notification templates only.
6. **No production config patch:** Block flags trigger if configuration overwrites are suggested.
7. **No dossier auto-enable:** Strict required manual reviews.

## Commands
- `python -m usa_signal_bot non-execution-compliance --write`
- `python -m usa_signal_bot promotion-dossier-validate --latest-review`
