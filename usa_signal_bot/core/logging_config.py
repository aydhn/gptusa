"""Logging configuration for USA Signal Bot."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

from usa_signal_bot.core.exceptions import LoggingSetupError
from usa_signal_bot.core.events import SystemEvent, event_to_dict
from usa_signal_bot.utils.text_utils import redact_sensitive_text

_LOGGING_CONFIGURED = False

def setup_logging(
    level: str = "INFO",
    log_dir: str = "data/logs",
    log_file: str = "app.log",
    enable_console: bool = True,
    enable_file: bool = True,
    max_bytes: int = 5000000,
    backup_count: int = 5
) -> None:
    """Sets up the global logging configuration."""
    global _LOGGING_CONFIGURED

    if _LOGGING_CONFIGURED:
        return

    numeric_level = getattr(logging, level.upper(), None)
    if not isinstance(numeric_level, int):
        raise LoggingSetupError(f"Invalid log level: {level}")

    root_logger = logging.getLogger()
    root_logger.setLevel(numeric_level)

    # Remove existing handlers to avoid duplicates if re-initialized
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if enable_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if enable_file:
        try:
            log_path_dir = Path(log_dir)
            if not log_path_dir.exists():
                log_path_dir.mkdir(parents=True, exist_ok=True)

            log_file_path = log_path_dir / log_file

            file_handler = RotatingFileHandler(
                log_file_path,
                maxBytes=max_bytes,
                backupCount=backup_count,
                encoding='utf-8'
            )
            file_handler.setLevel(numeric_level)
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
        except Exception as e:
            raise LoggingSetupError(f"Failed to setup file logging at {log_dir}/{log_file}: {e}")

    _LOGGING_CONFIGURED = True

def get_logger(name: str) -> logging.Logger:
    """Returns a logger instance with the given name."""
    return logging.getLogger(name)

def log_system_event(event: SystemEvent, logger: Optional[logging.Logger] = None) -> None:
    """Logs a system event using the appropriate log level."""
    log = logger or get_logger(event.component)

    msg = redact_sensitive_text(event.message)

    # Simple mapping from severity to logger method
    if event.severity == "DEBUG":
        log.debug(f"[EVENT:{event.event_type}] {msg}")
    elif event.severity == "INFO":
        log.info(f"[EVENT:{event.event_type}] {msg}")
    elif event.severity == "WARNING":
        log.warning(f"[EVENT:{event.event_type}] {msg}")
    elif event.severity == "ERROR":
        log.error(f"[EVENT:{event.event_type}] {msg}")
    elif event.severity == "CRITICAL":
        log.critical(f"[EVENT:{event.event_type}] {msg}")
    else:
        log.info(f"[EVENT:{event.event_type}] {msg}")
