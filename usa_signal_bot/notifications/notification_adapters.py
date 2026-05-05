import json
from pathlib import Path
from typing import List

from usa_signal_bot.notifications.notification_models import NotificationMessage
from usa_signal_bot.notifications.notification_templates import (
    format_scan_summary_message,
    format_selected_candidates_message,
    format_risk_decisions_message,
    format_portfolio_basket_message,
    format_runtime_warning_message,
    format_runtime_error_message
)
from usa_signal_bot.runtime.runtime_models import MarketScanResult
from usa_signal_bot.runtime.runtime_events import RuntimeEvent
from usa_signal_bot.core.enums import RuntimeEventType

def notifications_from_scan_result(scan_result: MarketScanResult) -> List[NotificationMessage]:
    messages = []
    messages.append(format_scan_summary_message(scan_result))
    return messages

def notifications_from_runtime_events(events: List[RuntimeEvent], include_warnings: bool = True, include_errors: bool = True) -> List[NotificationMessage]:
    messages = []
    warnings = []
    errors = []

    for event in events:
        if include_warnings and event.event_type == RuntimeEventType.WARNING:
            warnings.append(event.message)
        elif include_errors and event.event_type == RuntimeEventType.ERROR:
            errors.append(event.message)

    if warnings:
        messages.append(format_runtime_warning_message("Runtime Warnings Detected", warnings))
    if errors:
        messages.append(format_runtime_error_message("Runtime Errors Detected", errors))

    return messages

def notifications_from_selected_candidates_file(path: Path, limit: int = 10) -> List[NotificationMessage]:
    if not path.exists():
        return [format_runtime_warning_message("Missing Candidates", [f"File not found: {path.name}"])]

    try:
        candidates = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    candidates.append(json.loads(line))
        return [format_selected_candidates_message(candidates, limit)]
    except Exception as e:
        return [format_runtime_error_message("Candidate Parse Error", [str(e)])]

def notifications_from_risk_decisions_file(path: Path, limit: int = 10) -> List[NotificationMessage]:
    if not path.exists():
        return [format_runtime_warning_message("Missing Risk Decisions", [f"File not found: {path.name}"])]

    try:
        from usa_signal_bot.risk.risk_models import RiskDecision
        decisions = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    data = json.loads(line)
                    # Create a dummy object matching RiskDecision structure
                    class DummyDecision:
                        def __init__(self, d):
                            self.symbol = d.get("symbol", "UNKNOWN")
                            self.status = d.get("status", "UNKNOWN")
                            self.reasons = d.get("reasons", [])
                    decisions.append(DummyDecision(data))
        return [format_risk_decisions_message(decisions, limit)]
    except Exception as e:
        return [format_runtime_error_message("Risk Decision Parse Error", [str(e)])]

def notifications_from_portfolio_basket_file(path: Path, limit: int = 10) -> List[NotificationMessage]:
    if not path.exists():
        return [format_runtime_warning_message("Missing Portfolio Basket", [f"File not found: {path.name}"])]

    try:
        with open(path, "r", encoding="utf-8") as f:
            basket_data = json.load(f)

        allocations = basket_data.get("allocations", [])
        return [format_portfolio_basket_message(allocations, limit)]
    except Exception as e:
        return [format_runtime_error_message("Portfolio Basket Parse Error", [str(e)])]

def build_scan_notification_bundle(scan_result: MarketScanResult, include_candidates: bool = True, include_risk: bool = True, include_portfolio: bool = True) -> List[NotificationMessage]:
    bundle = notifications_from_scan_result(scan_result)

    paths = scan_result.output_paths

    if include_candidates and "selected_candidates" in paths:
        bundle.extend(notifications_from_selected_candidates_file(Path(paths["selected_candidates"])))

    if include_risk and "risk_decisions" in paths:
        bundle.extend(notifications_from_risk_decisions_file(Path(paths["risk_decisions"])))

    if include_portfolio and "portfolio_basket" in paths:
        bundle.extend(notifications_from_portfolio_basket_file(Path(paths["portfolio_basket"])))

    return bundle
