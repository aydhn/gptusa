# Locked Observer Runtime

The Locked Observer Runtime isolates the candidate strategy execution, providing a secure context where external mutations are blocked.

## Core Properties
*   **Locked by Design:** The runtime context is flagged as `locked=True`. There is no mechanism within the observer subsystem to unlock the context for live execution.
*   **Isolated State:** The runtime operates solely on an in-memory, read-only copy of the `paper_store` snapshot.
*   **Output Interception:** All outputs (signals, proposals, risks) are securely intercepted and routed to the `ObserverOutput` registry instead of the live message bus.

## Operations Blocked
The `blocked_operation_guard.py` explicitly denies:
*   `write_paper_state`
*   `send_paper_order`
*   `send_broker_order`
*   `send_telegram_real`
*   `write_production_config`
*   `enable_active_paper`
*   `unlock_observer_runtime`
*   `mutate_paper_store`

## CLI Usage
Inspect the default locked observer policy:
```bash
python -m usa_signal_bot locked-observer-policy --write
```

Generate a mocked, locked runtime context:
```bash
python -m usa_signal_bot observer-runtime-context --write
```
