# USA Signal Bot Environment Management

The USA Signal Bot utilizes system environment variables specifically for handling sensitive secrets.

## Telegram Notifications

If Telegram notifications are enabled (`telegram.enabled = true`), the bot requires specific environment variables to function correctly.

- `TELEGRAM_BOT_TOKEN`: The API Token for your Telegram Bot (provided by BotFather).
- `TELEGRAM_CHAT_ID`: The Chat ID where notifications should be sent.

By default, the bot configuration points to these exact environment variable names.

## How to Set Environment Variables

### Windows (PowerShell)
To set an environment variable temporarily in your current terminal session:
```powershell
$env:TELEGRAM_BOT_TOKEN="your_bot_token_here"
$env:TELEGRAM_CHAT_ID="your_chat_id_here"
```

### Linux / macOS (Bash/Zsh)
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token_here"
export TELEGRAM_CHAT_ID="your_chat_id_here"
```

## Security Best Practices
- **Never write tokens into `config/*.yaml` files.**
- Tokens are automatically redacted from CLI outputs via the `redact_sensitive_keys` utility.
- Tokens will never appear in application log files.
- Tokens will never be committed to Git.
