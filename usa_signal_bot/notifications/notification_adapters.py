
from typing import Optional, List, Dict, Any, Tuple
from usa_signal_bot.runtime.runtime_models import MarketScanResult
from usa_signal_bot.strategies.candidate_selection import SelectedCandidate
from usa_signal_bot.risk.risk_models import RiskRunResult
from usa_signal_bot.portfolio.portfolio_models import PortfolioConstructionResult
from usa_signal_bot.runtime.runtime_events import RuntimeEvent
from usa_signal_bot.notifications.alert_models import AlertEvaluationContext, AlertPolicyScope
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

def alert_context_from_scan_result(scan_result: MarketScanResult) -> AlertEvaluationContext:
    payload = {
        "run_id": scan_result.run_id,
        "status": scan_result.status.value if hasattr(scan_result.status, "value") else scan_result.status,
        "signal_count": scan_result.signal_count,
        "candidate_count": scan_result.candidate_count,
        "risk_approved_count": scan_result.risk_approved_count,
        "portfolio_allocation_count": scan_result.portfolio_allocation_count,
        "warnings_count": len(scan_result.warnings),
        "errors_count": len(scan_result.errors)
    }
    return AlertEvaluationContext(
        payload=payload,
        run_id=scan_result.run_id,
        scope=AlertPolicyScope.SCAN,
        source_path="scan_result"
    )

def alert_context_from_candidate_summary(run_id: Optional[str], candidates: List[SelectedCandidate]) -> AlertEvaluationContext:
    payload = {
        "run_id": run_id,
        "candidate_count": len(candidates),
        "symbols": [c.candidate_id for c in candidates]
    }
    return AlertEvaluationContext(
        payload=payload,
        run_id=run_id,
        scope=AlertPolicyScope.CANDIDATE,
        source_path="candidate_summary"
    )

def alert_context_from_risk_run_result(result: RiskRunResult) -> AlertEvaluationContext:
    payload = {
        "run_id": result.run_id,
        "status": result.status.value if hasattr(result.status, "value") else result.status,
        "approved_count": result.approved_count,
        "rejected_count": result.rejected_count,
        "reduced_count": result.reduced_count,
        "needs_review_count": result.needs_review_count
    }
    return AlertEvaluationContext(
        payload=payload,
        run_id=result.run_id,
        scope=AlertPolicyScope.RISK,
        source_path="risk_result"
    )

def alert_context_from_portfolio_result(result: PortfolioConstructionResult) -> AlertEvaluationContext:
    payload = {
        "run_id": result.run_id,
        "status": result.status.value if hasattr(result.status, "value") else result.status,
        "review_status": result.review_status.value if hasattr(result.review_status, "value") else result.review_status,
        "allocated_count": result.allocated_count,
        "rejected_count": result.rejected_count,
        "total_weight": result.metrics.get("total_weight", 0.0),
        "cash_buffer": result.metrics.get("cash_buffer", 0.0)
    }
    return AlertEvaluationContext(
        payload=payload,
        run_id=result.run_id,
        scope=AlertPolicyScope.PORTFOLIO,
        source_path="portfolio_result"
    )

def alert_context_from_runtime_events(run_id: Optional[str], events: List[RuntimeEvent]) -> AlertEvaluationContext:
    error_count = sum(1 for e in events if str(e.severity).lower() == "error")
    warning_count = sum(1 for e in events if str(e.severity).lower() == "warning")
    payload = {
        "run_id": run_id,
        "event_count": len(events),
        "error_count": error_count,
        "warning_count": warning_count
    }
    return AlertEvaluationContext(
        payload=payload,
        run_id=run_id,
        scope=AlertPolicyScope.RUNTIME,
        source_path="runtime_events"
    )

def alert_context_from_health_summary(summary: Dict[str, Any]) -> AlertEvaluationContext:
    payload = {
        "status": summary.get("overall_status", "unknown"),
        "total_checks": summary.get("total_checks", 0),
        "failed_checks": summary.get("failed_checks", 0)
    }
    return AlertEvaluationContext(
        payload=payload,
        run_id=summary.get("run_id"),
        scope=AlertPolicyScope.HEALTH,
        source_path="health_summary"
    )

def build_policy_driven_scan_notifications(scan_result: MarketScanResult, evaluator: Optional[Any] = None) -> Tuple['AlertEvaluationResult', List['NotificationMessage']]:

    from usa_signal_bot.notifications.alert_evaluator import AlertEvaluator
    evaluator = evaluator or AlertEvaluator()
    ctx = alert_context_from_scan_result(scan_result)
    return evaluator.evaluate_and_build_messages(ctx)
