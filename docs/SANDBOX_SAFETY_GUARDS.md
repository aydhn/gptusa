# Sandbox Safety Guards

USA Signal Bot strictly guards inputs mapping blocked behaviors and resolving execution failures inside memory to identify risks actively.

## Active Denied Scopes
- No broker/order fields
- No paper state mutation
- No Telegram real send logic
- No production config patches natively allowed.

Safety validations execute context logic preventing unsafe commands explicitly by parsing context language to eliminate phrases assuming success natively like: `live approved` and `production'a geçir`.

## Usage Examples
```bash
python -m usa_signal_bot sandbox-operation-guard --operation send_order
python -m usa_signal_bot sandbox-safety-validate --write
```
