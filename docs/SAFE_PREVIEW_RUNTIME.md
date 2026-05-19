# Safe Preview Runtime

The `SafePreviewRunner` guarantees deterministic outputs without network requests internally parsing data signals.

Previews included mock executions for:
* **Signal Generation**
* **Portfolio Risk Checks**
* **Drawdown & Regime Cost Metrics**
* **Notifications**

Output representations maintain a safe logic without generating active payloads mapping directly inside `data/release_sandbox/outputs`.

## Usage Examples
```bash
python -m usa_signal_bot sandbox-runtime-context --write
python -m usa_signal_bot sandbox-preview-run --runtime-mode full_safe_preview --write
```
