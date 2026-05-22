# Write Blocked Paper Runtime Adapter
Provides a read-only snapshot and blocks all write attempts (orders, config patching, state mutation) to prove that the runtime cannot execute active trades.
## Limits
- Does not modify paper state.
## Commands
`python -m usa_signal_bot write-blocked-snapshot --write`
`python -m usa_signal_bot write-blocked-attempt --attempt-type paper_state_write --write`
`python -m usa_signal_bot write-deny-proof --write`
