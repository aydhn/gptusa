from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import uuid
import datetime

from usa_signal_bot.core.enums import (
    PaperRuntimeSource,
    PaperExecutionMode,
    PaperRuntimeStatus
)
from usa_signal_bot.paper.paper_models import PaperEngineRunResult, paper_engine_run_result_to_dict

@dataclass
class PaperRuntimeRequest:
    request_id: str
    source: PaperRuntimeSource
    execution_mode: PaperExecutionMode
    account_name: str
    starting_cash: float
    timeframe: str
    risk_decisions_file: Optional[str] = None
    allocations_file: Optional[str] = None
    selected_candidates_file: Optional[str] = None
    signals_file: Optional[str] = None
    max_orders: Optional[int] = None
    write_outputs: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PaperRuntimeResult:
    result_id: str
    created_at_utc: str
    status: PaperRuntimeStatus
    request: PaperRuntimeRequest
    paper_run_result: Optional[PaperEngineRunResult]
    order_intent_count: int
    accepted_order_count: int
    filled_order_count: int
    rejected_order_count: int
    output_paths: Dict[str, str]
    warnings: List[str]
    errors: List[str]

@dataclass
class PaperRuntimeContext:
    scan_run_id: Optional[str]
    risk_decisions_file: Optional[str]
    portfolio_allocations_file: Optional[str]
    selected_candidates_file: Optional[str]
    signals_file: Optional[str]
    resolved_symbols: List[str]
    timeframe: str
    metadata: Dict[str, Any] = field(default_factory=dict)

def paper_runtime_request_to_dict(request: PaperRuntimeRequest) -> dict:
    from dataclasses import asdict
    d = asdict(request)
    d["source"] = request.source.value if hasattr(request.source, "value") else request.source
    d["execution_mode"] = request.execution_mode.value if hasattr(request.execution_mode, "value") else request.execution_mode
    return d

def paper_runtime_result_to_dict(result: PaperRuntimeResult) -> dict:
    from dataclasses import asdict
    d = asdict(result)
    d["status"] = result.status.value if hasattr(result.status, "value") else result.status
    d["request"] = paper_runtime_request_to_dict(result.request)
    if result.paper_run_result:
        d["paper_run_result"] = paper_engine_run_result_to_dict(result.paper_run_result)
    return d

def paper_runtime_context_to_dict(context: PaperRuntimeContext) -> dict:
    from dataclasses import asdict
    return asdict(context)

def validate_paper_runtime_request(request: PaperRuntimeRequest) -> None:
    if request.starting_cash <= 0:
        raise ValueError("starting_cash must be positive")
    if not request.timeframe:
        raise ValueError("timeframe cannot be empty")
    if request.max_orders is not None and request.max_orders <= 0:
        raise ValueError("max_orders must be None or positive")

    # Source validation
    if request.source == PaperRuntimeSource.SCAN_CONTEXT:
        if not any([request.risk_decisions_file, request.allocations_file, request.selected_candidates_file, request.signals_file]):
            raise ValueError("SCAN_CONTEXT source requires at least one input file")

def validate_paper_runtime_result(result: PaperRuntimeResult) -> None:
    pass

def create_paper_runtime_request_id(prefix: str = "paper_runtime_req") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_paper_runtime_result_id(prefix: str = "paper_runtime_result") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"
