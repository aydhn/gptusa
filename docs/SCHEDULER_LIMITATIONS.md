# Scheduler Limitations

This local implementation ensures extreme safety. These constraints are intentional:

- **No Daemons/Background Tasks**: This scheduler runs strictly "on demand" within the local Python runtime. It does NOT invoke `cron`, `systemd`, `Windows Services`, or keep a background process running without a user prompt.
- **No External Message Queue**: Everything runs locally and sequentially inside the process via local JSON logic.
- **File Lock Boundaries**: File locks protect cross-process clashes on the same machine but do not provide atomic distributed protections across different servers.
- **Stale Lock Overheads**: If a process crashes abruptly, the lock defaults to "stale" until explicitly cleared or stolen.
- **No Broker Communication**: The scheduler executes dry-run evaluations or data gathering. It explicitly lacks dependencies and integration code to route actual live/demo orders to Alpaca, IBKR, etc.
- **Not Investment Advice**: Outputs, plans, and successful "runs" do not constitute financial guidance, live trading authorization, or investment advice.
