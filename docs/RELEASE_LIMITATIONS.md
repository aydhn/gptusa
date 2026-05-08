# Release Limitations

The USA Signal Bot Local Release package imposes explicit limitations to enforce its local, non-trading nature:

1. **Not a Live Installer**: This package does not generate executable files (No PyInstaller, cx_Freeze).
2. **No Web/API Features**: Features no Flask/FastAPI servers, no web dashboard, no HTML parsing logic.
3. **No Direct Trading**: The runbook explicitly details that this release bundle does NOT perform live trading or connect to broker APIs (Alpaca, IBKR, etc.).
4. **Not Investment Advice**: Content produced, reports generated, and metrics assessed by the system are purely hypothetical backtests and analytics, not financial guidance.
5. **Secrets are EXCLUDED**: Backups and releases explicitly filter `.env`, `*token*`, and `*secret*` filenames.
