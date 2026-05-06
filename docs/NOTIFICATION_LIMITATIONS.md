# Notification Limitations

- Relies on constant internet connection for `allow_real_send = true` deployments.
- There is **no bidirectional communication** or conversational bot command handling included.
- Tokens must be managed entirely outside the Python configuration (via `env`).
- Hash-based deduplication is robust but strictly bound by the message text and window configuration parameter bounds.
- No live dashboards or persistent UI layers sit on top of the dispatcher.
