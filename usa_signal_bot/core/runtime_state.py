"""Runtime state tracking and context."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from usa_signal_bot.core.config_schema import AppConfig
from usa_signal_bot.core.exceptions import RuntimeInitializationError

@dataclass
class RuntimeContext:
    """Holds the active runtime state, configuration, and resolved paths."""
    config: AppConfig
    project_root: Path
    config_dir: Path
    data_dir: Path
    logs_dir: Path
    cache_dir: Path
    reports_dir: Path
    paper_dir: Path
    backtests_dir: Path
    started_at_utc: str
    execution_mode: str

    log_file_path: Optional[Path] = None
    audit_log_path: Optional[Path] = None
    health_status: Optional[str] = None

    def as_summary_dict(self) -> dict:
        """Returns a summarized dictionary of the runtime context."""
        return {
            "project_name": self.config.project.name,
            "version": self.config.project.version,
            "execution_mode": self.execution_mode,
            "started_at_utc": self.started_at_utc,
            "safe_mode": {
                "broker_routing_disabled": not self.config.runtime.broker_order_routing_enabled,
                "web_scraping_disabled": not self.config.runtime.web_scraping_allowed,
                "dashboard_disabled": not self.config.runtime.dashboard_enabled,
                "local_paper_only": self.config.runtime.mode == "local_paper_only"
            },
            "paths": {
                "project_root": str(self.project_root),
                "data_dir": str(self.data_dir),
                "logs_dir": str(self.logs_dir),
                "log_file_path": str(self.log_file_path) if self.log_file_path else None,
                "audit_log_path": str(self.audit_log_path) if self.audit_log_path else None
            },
            "health_status": self.health_status
        }

    def assert_safe_mode(self) -> None:
        """Asserts that all safety guards are correctly enforced in the context."""
        if self.config.runtime.broker_order_routing_enabled:
            raise RuntimeInitializationError("CRITICAL: Broker order routing is enabled in runtime context.")
        if self.config.runtime.web_scraping_allowed:
            raise RuntimeInitializationError("CRITICAL: Web scraping is allowed in runtime context.")
        if self.config.runtime.dashboard_enabled:
            raise RuntimeInitializationError("CRITICAL: Dashboard is enabled in runtime context.")
        if self.config.runtime.mode != "local_paper_only":
            raise RuntimeInitializationError("CRITICAL: Execution mode is not local_paper_only.")
