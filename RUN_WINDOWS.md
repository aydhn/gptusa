# Running USA Signal Bot on Windows

This guide explains how to start the USA Signal Bot on Windows using the provided startup script.

## Quick Start

1. Open a Command Prompt (CMD) or PowerShell in the root directory of the repository.
2. Run the startup script:
   ```cmd
   start_windows.bat
   ```

## What the Script Does

The `start_windows.bat` script automates the safe initialization and startup of the bot. It performs the following steps:

1. **Environment Verification:** Checks if Python is installed and if the script is run from the correct directory.
2. **Virtual Environment Setup:** Creates a Python virtual environment (`.venv`) if one doesn't exist, and verifies its integrity.
3. **Dependency Management:** Updates pip/setuptools/wheel and installs required dependencies from `requirements.txt` and `setup.py`.
4. **Configuration Wizard:** Checks for the `config\runtime.env` file. If it's missing, it creates a template and asks you to fill it in.
5. **Gitignore Checks:** Ensures `.venv`, `logs/`, and `*.env` are in your `.gitignore` to prevent committing sensitive data.
6. **Testing:** Runs basic smoke tests (`test_smoke.py`) to ensure the application imports correctly.
7. **Healthchecks:** Runs `scripts\windows_healthcheck.py` to verify Python version, dependencies, configuration, and directory permissions.
8. **Supervisor:** If all checks pass, it hands off to `scripts\windows_supervisor.py`, which starts the main bot process and restarts it if it crashes (up to a limit).

## Automatic Modules
- The `windows_healthcheck.py` script automatically verifies the environment.
- The `windows_supervisor.py` script automatically monitors and restarts the main application.

## Scheduled Modules
- Modules like `backtest`, `benchmark`, `optimizer`, and `walk-forward` are typically run manually or on a schedule, rather than as continuously running supervisor tasks. The current supervisor is configured to run the `ml-closure-info` command as an example, but you can modify it to run other continuous processes.

## Manual Modules
- You may need to manually fill in the `config\runtime.env` file with your specific API keys, Telegram tokens, and risk limits.

## Troubleshooting

- **Logs:** Check the `logs\` directory. `windows_startup.log` contains initialization details, `healthcheck.log` contains healthcheck results, and `errors.log` contains supervisor crash reports.
- **Virtual Environment Issues:** If you suspect the `.venv` is corrupted, delete it and run `start_windows.bat` again.
