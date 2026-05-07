from pathlib import Path
from typing import Any, Dict, List, Optional
import datetime
import uuid

from usa_signal_bot.core.enums import (
    PaperRuntimeSource, PaperExecutionMode, PaperRuntimeStatus, PaperEngineStatus
)
from usa_signal_bot.paper.paper_runtime_models import (
    PaperRuntimeRequest, PaperRuntimeResult, PaperRuntimeContext,
    create_paper_runtime_result_id
)
from usa_signal_bot.paper.paper_engine import PaperTradingEngine, PaperEngineConfig
from usa_signal_bot.paper.paper_adapters import (
    load_paper_order_intents_from_risk_decisions_file,
    load_paper_order_intents_from_allocations_file,
    load_paper_order_intents_from_selected_candidates_file,
    load_paper_order_intents_from_signals_file
)
from usa_signal_bot.paper.paper_models import PaperOrderIntent, PaperEngineRunResult

class PaperRuntimeRunner:
    def __init__(self, data_root: Path, engine: Optional[PaperTradingEngine] = None):
        self.data_root = data_root
        self.engine = engine

    def run(self, request: PaperRuntimeRequest) -> PaperRuntimeResult:
        intents = self.build_order_intents(request)

        result_id = create_paper_runtime_result_id()
        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        if not intents:
            return PaperRuntimeResult(
                result_id=result_id,
                created_at_utc=now_utc,
                status=PaperRuntimeStatus.EMPTY,
                request=request,
                paper_run_result=None,
                order_intent_count=0,
                accepted_order_count=0,
                filled_order_count=0,
                rejected_order_count=0,
                output_paths={},
                warnings=["No order intents generated from source."],
                errors=[]
            )

        if not self.engine:
            cfg = PaperEngineConfig(
                execution_mode=request.execution_mode,
                starting_cash=request.starting_cash,
                write_outputs=request.write_outputs
            )
            self.engine = PaperTradingEngine(self.data_root, config=cfg)

        paper_res = self.engine.run_order_intents(intents)

        status = PaperRuntimeStatus.COMPLETED
        if paper_res.status == PaperEngineStatus.FAILED:
            status = PaperRuntimeStatus.FAILED
        elif paper_res.status == PaperEngineStatus.PARTIAL_SUCCESS:
            status = PaperRuntimeStatus.PARTIAL_SUCCESS
        elif paper_res.status == PaperEngineStatus.EMPTY:
            status = PaperRuntimeStatus.EMPTY

        summary = self.summarize_paper_run(paper_res)

        res = PaperRuntimeResult(
            result_id=result_id,
            created_at_utc=now_utc,
            status=status,
            request=request,
            paper_run_result=paper_res,
            order_intent_count=len(intents),
            accepted_order_count=summary["accepted"],
            filled_order_count=summary["filled"],
            rejected_order_count=summary["rejected"],
            output_paths=paper_res.output_paths.copy(),
            warnings=paper_res.warnings,
            errors=paper_res.errors
        )

        return res

    def build_order_intents(self, request: PaperRuntimeRequest) -> List[PaperOrderIntent]:
        intents = []

        if request.source == PaperRuntimeSource.PORTFOLIO_ALLOCATIONS and request.allocations_file:
            intents = load_paper_order_intents_from_allocations_file(Path(request.allocations_file))
        elif request.source == PaperRuntimeSource.RISK_DECISIONS and request.risk_decisions_file:
            intents = load_paper_order_intents_from_risk_decisions_file(Path(request.risk_decisions_file))
        elif request.source == PaperRuntimeSource.SELECTED_CANDIDATES and request.selected_candidates_file:
            intents = load_paper_order_intents_from_selected_candidates_file(Path(request.selected_candidates_file))
        elif request.source == PaperRuntimeSource.SIGNALS and request.signals_file:
            intents = load_paper_order_intents_from_signals_file(Path(request.signals_file))
        elif request.source == PaperRuntimeSource.SCAN_CONTEXT:
            if request.allocations_file:
                intents = load_paper_order_intents_from_allocations_file(Path(request.allocations_file))
            elif request.risk_decisions_file:
                intents = load_paper_order_intents_from_risk_decisions_file(Path(request.risk_decisions_file))
            elif request.selected_candidates_file:
                intents = load_paper_order_intents_from_selected_candidates_file(Path(request.selected_candidates_file))
            elif request.signals_file:
                intents = load_paper_order_intents_from_signals_file(Path(request.signals_file))

        if request.max_orders and len(intents) > request.max_orders:
            intents = intents[:request.max_orders]

        return intents

    def build_request_from_scan_context(
        self,
        context: PaperRuntimeContext,
        execution_mode: PaperExecutionMode = PaperExecutionMode.DRY_RUN,
        starting_cash: float = 100000.0,
        max_orders: Optional[int] = None
    ) -> PaperRuntimeRequest:

        req = PaperRuntimeRequest(
            request_id=f"paper_req_{uuid.uuid4().hex[:8]}",
            source=PaperRuntimeSource.SCAN_CONTEXT,
            execution_mode=execution_mode,
            account_name=f"scan_{context.scan_run_id}" if context.scan_run_id else "scan_paper",
            starting_cash=starting_cash,
            timeframe=context.timeframe,
            risk_decisions_file=context.risk_decisions_file,
            allocations_file=context.portfolio_allocations_file,
            selected_candidates_file=context.selected_candidates_file,
            signals_file=context.signals_file,
            max_orders=max_orders,
            write_outputs=True,
            metadata={"scan_run_id": context.scan_run_id}
        )
        return req

    def run_from_scan_context(
        self,
        context: PaperRuntimeContext,
        execution_mode: PaperExecutionMode = PaperExecutionMode.DRY_RUN,
        starting_cash: float = 100000.0,
        max_orders: Optional[int] = None
    ) -> PaperRuntimeResult:
        req = self.build_request_from_scan_context(context, execution_mode, starting_cash, max_orders)
        return self.run(req)

    def summarize_paper_run(self, result: Optional[PaperEngineRunResult]) -> Dict[str, Any]:
        if not result:
            return {"accepted": 0, "filled": 0, "rejected": 0}

        from usa_signal_bot.core.enums import PaperOrderStatus
        accepted = sum(1 for o in result.orders if o.status in [PaperOrderStatus.ACCEPTED, PaperOrderStatus.QUEUED, PaperOrderStatus.FILLED, PaperOrderStatus.PARTIALLY_FILLED])
        filled = sum(1 for o in result.orders if o.status == PaperOrderStatus.FILLED)
        rejected = sum(1 for o in result.orders if o.status == PaperOrderStatus.REJECTED)

        return {
            "accepted": accepted,
            "filled": filled,
            "rejected": rejected
        }

    def write_runtime_result(self, result: PaperRuntimeResult) -> List[Path]:
        return []
