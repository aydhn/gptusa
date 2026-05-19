# Shadow Safety Guards

The Shadow Safety Guards are the ultimate protection mechanism ensuring that the shadow rehearsal remains purely simulated.

## Checked Risks
- **Real Order Risk:** The system asserts that `allow_real_orders` is False in the context, and `is_real_order` is False in intents.
- **Paper State Mutation Risk:** The system asserts that `allow_paper_state_mutation` is False. It also verifies that the `paper_store` and other stateful components are not updated during the run.
- **Telegram Real Send Risk:** The system asserts that `allow_telegram_real_send` is False to prevent sending mock data as real notifications.
- **Broker Field Risk:** Intents and Fills must not contain broker-specific metadata like `broker_order_id` or `sent_to_broker`.

## Command Line Interface (CLI)
```bash
python -m usa_signal_bot shadow-safety-check --write
python -m usa_signal_bot paper-shadow-validate --latest-review
```
