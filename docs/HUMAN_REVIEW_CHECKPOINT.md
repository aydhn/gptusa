# Human Review Checkpoint

## Purpose
The human review checkpoint enforces an explicit sign-off step before any further considerations (like transitioning to active paper) can even be debated.

## Features
- **Status tracking**: Tracks status (`required`, `waiting_review`, `reviewed_with_notes`, etc.).
- **Review Notes**: Maintains reviewer notes inside the checkpoint.
- **Strict Limitation**: An `ACCEPTED_FOR_OBSERVATION_ONLY` status does not grant live trading approval or permission to edit active paper state.

## CLI Usage
```bash
python -m usa_signal_bot human-review-checkpoint --write
python -m usa_signal_bot human-checkpoint-validate --write
```
