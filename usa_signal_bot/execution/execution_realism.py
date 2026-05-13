import datetime
from typing import Any, Optional, List

from usa_signal_bot.core.enums import (
    ExecutionRealismStatus,
    ExecutionReportType,
    TradabilityStatus
)
from usa_signal_bot.execution.liquidity_models import (
    ExecutionRealismReview,
    TradabilityGuardResult,
    create_execution_realism_review_id
)
from usa_signal_bot.execution.tradability_guard import TradabilityGuard
from usa_signal_bot.execution.borrowability_proxy import estimate_borrowability_proxy
from usa_signal_bot.providers.provider_models import ProviderResponse

class ExecutionRealismEvaluator:
    def __init__(self, guard: TradabilityGuard | None = None):
        self.guard = guard or TradabilityGuard()

    def decide_review_status(self, results: list[TradabilityGuardResult]) -> ExecutionRealismStatus:
        if not results:
            return ExecutionRealismStatus.INSUFFICIENT_DATA

        status_counts = {
            TradabilityStatus.BLOCK_SIGNAL: 0,
            TradabilityStatus.BLOCK_BACKTEST_FILL: 0,
            TradabilityStatus.REVIEW_REQUIRED: 0,
            TradabilityStatus.CAUTION: 0,
            TradabilityStatus.TRADABLE: 0
        }

        for r in results:
            if r.status in status_counts:
                status_counts[r.status] += 1

        total = len(results)

        if status_counts[TradabilityStatus.BLOCK_SIGNAL] > 0:
            return ExecutionRealismStatus.UNREALISTIC

        if status_counts[TradabilityStatus.REVIEW_REQUIRED] > total * 0.1:
            return ExecutionRealismStatus.OPTIMISTIC

        if status_counts[TradabilityStatus.CAUTION] > 0 or status_counts[TradabilityStatus.BLOCK_BACKTEST_FILL] > 0:
            return ExecutionRealismStatus.ACCEPTABLE_WITH_WARNINGS

        return ExecutionRealismStatus.REALISTIC

    def evaluate_symbol_payload(
        self,
        symbol_payload: dict[str, list[dict[str, Any]]],
        side: str = "long",
        notional_usd: float | None = None
    ) -> ExecutionRealismReview:

        now_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()

        tradability_results = self.guard.evaluate_many(symbol_payload, side, notional_usd)

        liquidity_profiles = [r.liquidity_profile for r in tradability_results if r.liquidity_profile]

        borrowability_results = []
        if side.lower() == "short":
            for symbol, rows in symbol_payload.items():
                b = estimate_borrowability_proxy(symbol, rows)
                borrowability_results.append(b)

        warnings = []
        if not symbol_payload:
            warnings.append("Empty payload. Insufficient data to evaluate.")

        review = ExecutionRealismReview(
            review_id=create_execution_realism_review_id(),
            created_at_utc=now_utc,
            report_type=ExecutionReportType.FULL_EXECUTION_REVIEW,
            symbols=list(symbol_payload.keys()),
            liquidity_profiles=liquidity_profiles,
            tradability_results=tradability_results,
            borrowability_results=borrowability_results,
            output_paths={},
            warnings=warnings,
            errors=[]
        )

        return review

    def evaluate_provider_response(
        self,
        response: ProviderResponse,
        side: str = "long",
        notional_usd: float | None = None
    ) -> ExecutionRealismReview:

        symbol_payload = {}
        for item in response.data:
            sym = item.get("symbol")
            if sym:
                if sym not in symbol_payload:
                    symbol_payload[sym] = []
                symbol_payload[sym].append(item)

        return self.evaluate_symbol_payload(symbol_payload, side, notional_usd)

    def summarize_review(self, review: ExecutionRealismReview) -> dict[str, Any]:
        return {
            "review_id": review.review_id,
            "created_at_utc": review.created_at_utc,
            "symbol_count": len(review.symbols),
            "blocked_signals": sum(1 for r in review.tradability_results if r.status == TradabilityStatus.BLOCK_SIGNAL),
            "review_required": sum(1 for r in review.tradability_results if r.status == TradabilityStatus.REVIEW_REQUIRED),
            "caution_required": sum(1 for r in review.tradability_results if r.status == TradabilityStatus.CAUTION),
            "tradable": sum(1 for r in review.tradability_results if r.status == TradabilityStatus.TRADABLE),
            "status": self.decide_review_status(review.tradability_results).value
        }
