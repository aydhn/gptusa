# Safe Runtime Controller

## Safety Guards
- **Stale Lock Mitigation**: Prevents frozen pipelines.
- **Step Checkpoints**: Graceful stops occur between steps when requested.
- **Failure Isolation**: A required step failure terminates the run safely, while an optional step failure only issues a warning.
- **Max Duration Guard**: Configurable limits restrict runaway processes.

## Restrictions
- The runtime controller strictly produces data artifacts.
- No live orders, broker routing, or paper trade execution.
