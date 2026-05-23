# Paper Sandbox Bridge Dry Run

The Paper Sandbox Bridge Dry Run serves as a metadata-only execution preview mechanism.
It is explicitly NOT an active paper trading activation.
It consumes Transition Dossiers and Bridge Envelopes to produce safe simulations of bridge routes without touching the real paper runtime.

## CLI Examples
`python -m usa_signal_bot bridge-dry-run-info`
`python -m usa_signal_bot bridge-dry-run-plan --write`
`python -m usa_signal_bot bridge-dry-run --write`
