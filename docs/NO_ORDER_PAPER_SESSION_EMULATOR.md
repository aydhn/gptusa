# No-Order Paper Session Emulator

The No-Order Paper Session Emulator simulates paper session states without issuing any orders or mutating the true paper state.
It guarantees `order_created=false` and `mutation_detected=false`.
It is NOT a real paper runtime.

## CLI Examples
`python -m usa_signal_bot no-order-session --write`
`python -m usa_signal_bot no-order-session-analyze --write`
