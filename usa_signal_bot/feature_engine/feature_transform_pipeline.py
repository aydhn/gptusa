import datetime
from typing import Any
from usa_signal_bot.core.enums import FeatureOutputKind
from usa_signal_bot.feature_engine.phase116_models import (
    FeatureComputationRequest, FeatureComputationResult, FeatureRegistry,
    FeatureInputContract, FeatureOutputSchema, create_feature_computation_result_id
)

class FeatureTransformPipeline:
    def __init__(
        self,
        registry: FeatureRegistry | None = None,
        input_contract: FeatureInputContract | None = None,
        output_schema: FeatureOutputSchema | None = None
    ):
        self.registry = registry
        self.input_contract = input_contract
        self.output_schema = output_schema

    def plan(self, request: FeatureComputationRequest) -> FeatureComputationResult:
        return FeatureComputationResult(
            result_id=create_feature_computation_result_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat(),
            request_id=request.request_id,
            symbol=request.symbol,
            computed_feature_count=len(request.feature_names),
            computed_factor_count=len(request.factor_names),
            planned_only=True,
            metadata_only=True,
            dry_run_only=True,
            research_data_only=True,
            output_kinds=[FeatureOutputKind.FEATURE_PLAN],
            produced_trade_signal=False,
            produced_order_decision=False,
            network_used=False,
            paid_api_used=False,
            scraping_used=False,
            html_parsing_used=False,
            broker_used=False,
            order_created=False,
            paper_state_mutated=False,
            telegram_real_sent=False,
            dashboard_started=False,
            passed=True,
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={"planned": True}
        )

    def plan_batch(self, requests: list[FeatureComputationRequest]) -> list[FeatureComputationResult]:
        return [self.plan(req) for req in requests]

    def validate_request(self, request: FeatureComputationRequest) -> list[str]:
        return []

    def validate_result(self, result: FeatureComputationResult) -> list[str]:
        errors = []
        if not result.planned_only:
            errors.append("planned_only must be true")
        if result.produced_trade_signal:
            errors.append("produced_trade_signal must be false")
        if result.produced_order_decision:
            errors.append("produced_order_decision must be false")
        if result.network_used:
            errors.append("network_used must be false")
        return errors

    def pipeline_summary(self, results: list[FeatureComputationResult]) -> dict[str, Any]:
        return {"total_results": len(results)}
