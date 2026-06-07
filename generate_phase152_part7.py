import os
import textwrap

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(textwrap.dedent(content).lstrip())

# 23-24 SCHEMA AND SAFETY VALIDATORS
write_file("usa_signal_bot/backtesting/closure/closure_schema_validator.py", """
from typing import Any
import pandas

def validate_closure_column_names(columns: list[str]) -> list[str]:
    return validate_no_forbidden_closure_columns(columns)

def validate_no_forbidden_closure_columns(columns: list[str]) -> list[str]:
    errors = []
    forbidden = [
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "order", "broker_order", "paper_order", "live_order", "live_signal", "buy_signal", "sell_signal"
    ]
    for col in columns:
        if any(f in col.lower() for f in forbidden):
            errors.append(f"Forbidden column name detected: {col}")
    return errors

def closure_schema_summary(errors: list[str]) -> dict[str, Any]:
    return {"valid": len(errors) == 0, "errors": errors}

def closure_schema_to_text(errors: list[str]) -> str:
    return "Valid" if not errors else f"Invalid: {', '.join(errors)}"
""")

write_file("usa_signal_bot/backtesting/closure/closure_safety_validator.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestClosureRiskFlag, BacktestClosureContext, BacktestFinalAuditReport,
    BacktestBandClosureCertificate, Phase153HandoffContract, Phase153HandoffPackage,
    HandoffSafetyBoundaryResult, Phase153ReadinessGate
)

def closure_text_has_trade_or_execution_language(text: str) -> bool:
    bad_phrases = [
        "is investment advice", "guaranteed profit", "sure thing", "buy now",
        "sell now", "execute immediately", "send to broker", "deploy to production"
    ]
    t = text.lower()
    for phrase in bad_phrases:
        if phrase in t:
            return True
    return False

def handoff_payload_has_forbidden_fields(payload: dict[str, Any]) -> bool:
    import json
    text = json.dumps(payload).lower()
    forbidden = [
        "portfolio_weight", "target_weight", "allocation", "position_size",
        "order", "broker_order", "paper_order", "live_order", "live_signal", "buy_signal", "sell_signal"
    ]
    for field in forbidden:
        if f'"{field}"' in text:
            return True
    return False

def closure_safety_summary(errors: list[str]) -> dict[str, Any]:
    return {"safe": len(errors) == 0, "errors": errors}

def closure_safety_to_text(errors: list[str]) -> str:
    return "Safe" if not errors else f"Unsafe: {', '.join(errors)}"
""")

# 25. REPORTING AND ORCHESTRATION
write_file("usa_signal_bot/backtesting/closure/backtest_closure_report.py", """
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestClosureContext, BacktestClosureFullReview, BacktestClosureReportType
)

def build_backtest_closure_context() -> BacktestClosureContext:
    # A simplified mock builder
    from usa_signal_bot.backtesting.closure.backtest_closure_orchestrator import build_safe_phase152_gate

    ctx = BacktestClosureContext()
    ctx.phase153_readiness_gate = build_safe_phase152_gate()
    ctx.phase153_readiness_gate_passed = ctx.phase153_readiness_gate.ready_for_phase153
    ctx.ready_for_phase153 = ctx.phase153_readiness_gate_passed
    return ctx

def build_backtest_closure_full_review() -> BacktestClosureFullReview:
    rev = BacktestClosureFullReview()
    rev.report_type = BacktestClosureReportType.FULL_PHASE152_REVIEW
    rev.context = build_backtest_closure_context()
    rev.phase153_readiness_gate = rev.context.phase153_readiness_gate
    return rev

def backtest_closure_full_review_summary(review: BacktestClosureFullReview) -> dict[str, Any]:
    return {"id": review.review_id, "ready_for_phase153": review.context.ready_for_phase153}

def backtest_closure_limitations_text() -> str:
    return "Phase 152 is a read-only final audit and closure phase. It does not perform active trading, deployment, portfolio construction, or optimization. The generated handoff package is for research purposes only."

def backtest_closure_full_review_to_text(review: BacktestClosureFullReview, limit: int = 300) -> str:
    return f"BacktestClosureFullReview: Ready for Phase 153 = {review.context.ready_for_phase153}"
""")

write_file("usa_signal_bot/backtesting/closure/backtest_closure_store.py", """
import json
from pathlib import Path
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import *

def backtest_closure_store_dir(data_root: Path) -> Path:
    return data_root / "backtesting" / "closure"

def backtest_closure_reviews_dir(data_root: Path) -> Path:
    return backtest_closure_store_dir(data_root) / "reviews"

def write_backtest_closure_full_review_json(path: Path, item: BacktestClosureFullReview) -> Path:
    import dataclasses

    def dc_default(o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        elif hasattr(o, "name"): # Enum
            return o.name
        return str(o)

    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(dataclasses.asdict(item), f, default=dc_default, indent=2)
    return path

def backtest_closure_store_summary(data_root: Path) -> dict[str, Any]:
    return {"dir": str(backtest_closure_store_dir(data_root))}
""")

write_file("usa_signal_bot/backtesting/closure/backtest_closure_validation.py", """
from typing import Any
from dataclasses import dataclass, field

@dataclass
class BacktestClosureValidationIssue:
    severity: str
    field: str | None
    message: str
    details: dict[str, Any] = field(default_factory=dict)

@dataclass
class BacktestClosureValidationReport:
    valid: bool = True
    issue_count: int = 0
    warning_count: int = 0
    error_count: int = 0
    blocked_count: int = 0
    issues: list[BacktestClosureValidationIssue] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_no_sensitive_data_in_closure_payload(payload: dict[str, Any]) -> BacktestClosureValidationReport:
    return BacktestClosureValidationReport()

def assert_backtest_closure_validation_valid(report: BacktestClosureValidationReport) -> None:
    if not report.valid:
        raise ValueError("Validation failed")
""")

write_file("usa_signal_bot/backtesting/closure/backtest_closure_reporting.py", """
from typing import Any

def backtest_closure_limitations_text() -> str:
    from usa_signal_bot.backtesting.closure.backtest_closure_report import backtest_closure_limitations_text
    return backtest_closure_limitations_text()
""")
