# NON-EXECUTION BOARD SAFETY GUARDS

Bu doküman, Non-Execution Board etrafına kurulan güvenlik korkuluklarını listeler.

- No active paper enable.
- No paper admission.
- No paper state mutation.
- No paper order.
- No broker order.
- No Telegram real send.
- No production config patch.
- Runtime map replay failed ise block.
- Non-execution seal integrity failed ise block.
- Board assertion failed ise block.
- admission_allowed true ise block.
- activation_allowed true ise block.
- order_created true ise block.
- mutation_detected true ise block.

## CLI Örnekleri
```bash
python -m usa_signal_bot --non-execution-board-continuity
python -m usa_signal_bot --non-execution-board-safety-check
python -m usa_signal_bot --non-execution-board-payload-validate
```
