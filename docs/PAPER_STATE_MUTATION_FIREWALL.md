# Paper-State Mutation Firewall

The Paper-State Mutation Firewall acts as a metadata-level defense system preventing unauthorized mutations during the pre-paper dry rehearsal stage.

**IMPORTANT LIMITATIONS:**
- **The mutation firewall operates purely at the metadata-level and does NOT write to the real paper runtime.**
- **Events are recorded for validation purposes and do not mutate state.**

## Blocked Operations
- PAPER_STATE_WRITE
- PAPER_ORDER_CREATE
- PAPER_POSITION_MUTATION
- PAPER_PORTFOLIO_MUTATION
- PAPER_CASH_MUTATION
- PAPER_EQUITY_MUTATION
- PAPER_FILL_CREATE
- BROKER_ORDER_SEND
- TELEGRAM_REAL_SEND
- PRODUCTION_CONFIG_PATCH
- ACTIVE_PAPER_ENABLE
- OBSERVER_UNLOCK
- ARCHIVE_UNLOCK
- FINAL_LOCK_UNLOCK

## CLI Usage

List firewall rules:
```bash
python -m usa_signal_bot mutation-firewall-rules --write
```

Evaluate an attempt type:
```bash
python -m usa_signal_bot mutation-firewall-evaluate --attempt-type paper_state_write --write
```

Simulate forbidden operations:
```bash
python -m usa_signal_bot forbidden-operation-simulate --write
```
