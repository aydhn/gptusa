from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.core.enums import SourceBlendMethod, SourceBlendStatus, ProviderOrchestrationRiskFlag
from usa_signal_bot.provider_orchestration.phase110_models import (
    SourceBlendInput, SourceBlendResult, create_source_blend_input_id,
    create_source_blend_result_id, validate_source_blend_result
)
from usa_signal_bot.provider_orchestration.source_blending_policy import source_blending_method_from_inputs

class SourceBlendingEngine:
    def build_blend_input(self, symbol: str, provider_payloads: dict[str, list[dict[str, Any]]],
                          quality_scores: dict[str, float], trust_scores: dict[str, float],
                          method: SourceBlendMethod | None = None) -> SourceBlendInput:
        if method is None:
            method = source_blending_method_from_inputs(len(provider_payloads))

        return SourceBlendInput(
            blend_input_id=create_source_blend_input_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            symbol=symbol,
            capability="GET_DAILY_OHLCV",
            interval="1d",
            source_provider_names=list(provider_payloads.keys()),
            source_quality_scores=quality_scores,
            source_trust_scores=trust_scores,
            source_records=provider_payloads,
            blend_method=method,
            tolerance_pct=0.01,
            dry_run_only=True,
            research_data_only=True,
            metadata={}
        )

    def blend(self, input_item: SourceBlendInput) -> SourceBlendResult:
        res = SourceBlendResult(
            blend_result_id=create_source_blend_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            blend_input_id=input_item.blend_input_id,
            symbol=input_item.symbol,
            status=SourceBlendStatus.UNKNOWN,
            method=input_item.blend_method,
            selected_primary_source=None,
            produces_trade_signal=False,
            produces_order_decision=False,
            dry_run_only=True,
            research_data_only=True,
            network_used=False,
            paid_api_used=False,
            scraping_used=False,
            html_parsing_used=False,
            broker_used=False,
            order_created=False,
            paper_state_mutated=False,
            telegram_real_sent=False,
            dashboard_started=False,
            metadata={}
        )

        sources = input_item.source_provider_names

        if not sources:
            res.status = SourceBlendStatus.INSUFFICIENT_SOURCES
            res.method = SourceBlendMethod.NO_BLEND
            return res

        if input_item.blend_method in (SourceBlendMethod.PRIMARY_ONLY, SourceBlendMethod.NO_BLEND) or len(sources) < 2:
            res.status = SourceBlendStatus.NOT_REQUIRED
            res.selected_primary_source = sources[0]
            res.included_sources = [sources[0]]
        else:
            res.status = SourceBlendStatus.BLENDED_METADATA_ONLY
            res.included_sources = sources
            res.confidence_score = 0.95

        errors = self.validate_blend_result_safety(res)
        if errors:
            res.errors.extend(errors)
            res.status = SourceBlendStatus.BLOCKED

        validate_source_blend_result(res)
        return res

    def blend_batch(self, inputs: list[SourceBlendInput]) -> list[SourceBlendResult]:
        return [self.blend(i) for i in inputs]

    def validate_blend_result_safety(self, result: SourceBlendResult) -> list[str]:
        errors = []
        if result.produces_trade_signal: errors.append("produces_trade_signal must be False")
        if result.produces_order_decision: errors.append("produces_order_decision must be False")
        if result.network_used: errors.append("network_used must be False")
        return errors

def source_blending_summary(results: list[SourceBlendResult]) -> dict[str, Any]:
    return {
        "total": len(results),
        "blended": sum(1 for r in results if r.status == SourceBlendStatus.BLENDED_METADATA_ONLY),
        "blocked": sum(1 for r in results if r.status == SourceBlendStatus.BLOCKED)
    }
