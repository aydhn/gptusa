# Dependency Contracts

Dependency Contracts act as formal agreements between service nodes, describing dependencies and allowed operations.

## Features
- **Strict Capabilities:** Explicitly define what capabilities a target service is allowed to expose.
- **No Execution Routes:** A contract fundamentally denies operations like `allows_execution`, `allows_broker`, `allows_order`, `allows_paper_mutation`, `allows_telegram_real_send`.
- **Validation:** Contracts are checked for cyclic dependencies and unsafe routing. If an invalid contract is found, the whole Service Graph is marked `BLOCKED`.
