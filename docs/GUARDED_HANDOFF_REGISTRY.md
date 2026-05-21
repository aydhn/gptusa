# Guarded Handoff Registry

The Guarded Handoff Registry records candidates that have passed the Staged Readiness Rehearsal and received a Final Review Lock, registering them for the final non-executing handoff review.

### Limitations
- **No Active Enablement**: Registration in the handoff registry does not enable active paper trading.
- **Evidence Verification**: Requires a complete Handoff Evidence Index.

### CLI Commands
- `python -m usa_signal_bot handoff-evidence-index --write`
- `python -m usa_signal_bot guarded-handoff-register --write`
