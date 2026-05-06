# Safe Notification Queue

## Mechanics
- **Queue Operation:** Pure FIFO queue that acts as an isolated pipeline layer after orchestration completes its scan steps.
- **De-Duplication:** Uses `NotificationDeduplicator` utilizing SHA-256 hash sets over predefined rolling windows to prevent flooding notifications about the same symbol logic recursively.
- **Rate Limit:** Built-in configurable limits enforce max messages per minute to abide by API gateway rules locally.

## CLI Interaction
`python -m usa_signal_bot notification-dispatch-dry-run --count 3`
