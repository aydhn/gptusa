# Final Review Lock

The Final Review Lock mechanism secures a successful readiness rehearsal by generating an immutable cryptographic hash of the execution artifacts.

### Limitations
- **Not an Approval**: A lock merely indicates that the readiness rehearsal completed successfully without execution errors. It is *not* a deployment approval.
- **No Activation**: A lock does not enable active paper trading.

### CLI Commands
- `python -m usa_signal_bot final-review-lock --write`
- `python -m usa_signal_bot final-lock-validate --write`
