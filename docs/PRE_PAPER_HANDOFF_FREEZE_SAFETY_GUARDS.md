# Pre-Paper Handoff Freeze Safety Guards

## Security Boundaries & Prohibitions
To ensure strict isolation from execution networks and external state manipulation, Phase 100 enforces the following safety guards during the handoff process:

- **No active paper enable:** Never authorizes active paper mode.
- **No paper admission:** Rejects requests to officially admit a candidate into active paper.
- **No simulator admission:** Blocks simulator entries.
- **No local paper simulator start:** Prevents starting of the local paper simulator.
- **No sandbox runtime admission:** Halts admission into the sandbox runtime environment.
- **No paper sandbox runtime start:** Refuses to launch paper sandbox execution threads.
- **No paper state mutation:** Stops any alteration of established paper state configurations.
- **No paper order:** Forbids construction or registration of paper orders.
- **No broker order:** Completely disconnects any pathway to live or demo broker orders.
- **No Telegram real send:** Telegram communications are preview only.
- **No production config patch:** Blockers prevent writes to production configuration endpoints.

## Blocking Conditions
The process will immediately fail and block progression if:
- A Sandbox runtime admission replay discovers any allowed attempts.
- A Simulator evidence freeze is missing (`failed`) or outdated (`stale`).
- A Handoff freeze assertion fails.
- Any of the critical parameters are incorrectly flagged as `True`:
  - `sandbox_runtime_admission_allowed`
  - `paper_sandbox_runtime_allowed`
  - `simulator_admission_allowed`
  - `local_paper_simulator_allowed`
  - `admission_allowed`
  - `activation_allowed`
  - `order_created`
  - `mutation_detected`

## CLI Usage
- Check continuity (ensuring all validations align properly over the chain):
  `python -m usa_signal_bot handoff-freeze-continuity --write`
- Verify the comprehensive safety state:
  `python -m usa_signal_bot handoff-freeze-safety-check --write`
- Perform a thorough validation against the most recent complete review:
  `python -m usa_signal_bot handoff-freeze-validate --latest-review`
