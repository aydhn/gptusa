"""Runtime initialization and bootstrapping."""

import logging
from typing import Dict, Any

from usa_signal_bot.core.paths import ensure_directories
from usa_signal_bot.core.config import load_config
from usa_signal_bot.core.logging_config import setup_logging

def init_runtime() -> Dict[str, Any]:
    """
    Initializes the runtime environment:
    - Ensures directories exist.
    - Loads and validates configuration.
    - Sets up logging.

    Returns:
        The validated configuration dictionary.
    """
    ensure_directories()

    config = load_config()

    log_level = config.get("logging", {}).get("level", "INFO")
    log_file = config.get("logging", {}).get("log_file", "app.log")

    setup_logging(level=log_level, log_file=log_file)

    logger = logging.getLogger(__name__)
    logger.debug("Runtime initialized successfully.")

    return config
