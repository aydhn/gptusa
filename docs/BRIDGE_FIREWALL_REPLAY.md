# Bridge Firewall Replay

The Bridge Firewall Replay verifies that dangerous operations are denied by the firewall.
It is a metadata-only check that simulates route attempts.
If any dangerous route is allowed, the firewall replay fails and blocks further operations.

## CLI Examples
`python -m usa_signal_bot bridge-replay-plan --write`
`python -m usa_signal_bot bridge-route-attempts --write`
`python -m usa_signal_bot bridge-firewall-replay --write`
