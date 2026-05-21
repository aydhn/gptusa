# Readiness Rehearsal Safety Guards

The Readiness Rehearsal enforces strict constraints to prevent accidental live execution.

- **No Active Paper Enablement**: Cannot set active paper flags to true.
- **No Paper State Mutation**: Cannot write to paper state store.
- **No Paper or Broker Orders**: No order logic allowed.
- **No Telegram Real Send**: Notifications are strictly dry-run previews.
- **No Production Config Patching**: System configuration is read-only.
- **No Auto-Enablement**: Final lock and handoff do not trigger automatic promotion.

### CLI Commands
- `python -m usa_signal_bot stage-safety-validate --write`
- `python -m usa_signal_bot readiness-rehearsal-validate --latest-review`
