# Activation-Denied Checkpoint

The Activation-Denied Checkpoint guarantees that the completion of the guarded pre-paper dry rehearsal does not automatically enable the active paper runtime.

**IMPORTANT:**
- `activation_denied` is strictly forced to `true`.
- **This checkpoint does NOT provide active paper/live/demo approval.**

## Checkpoint Rules
- Denied by default.
- Allows for required follow-ups, such as zero-mutation audits and safety reviews.

## CLI Usage

Generate the activation-denied checkpoint:
```bash
python -m usa_signal_bot activation-denied-checkpoint --write
```

Validate the checkpoint:
```bash
python -m usa_signal_bot activation-checkpoint-validate --write
```
