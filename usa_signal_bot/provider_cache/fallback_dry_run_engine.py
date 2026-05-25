from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.provider_cache.phase108_models import (
    FallbackDryRunPlan,
    FallbackDryRunResult,
    ProviderCacheIndex,
    StaleFreshPolicy,
    create_fallback_dry_run_result_id,
    FallbackDryRunStatus,
    FallbackDryRunDecision,
    ProviderCacheRiskFlag
)
from usa_signal_bot.provider_cache.fallback_chain_evaluator import evaluate_fallback_chain

class ProviderFallbackDryRunEngine:
    def __init__(self, cache_index: ProviderCacheIndex | None = None, policy: StaleFreshPolicy | None = None):
        self.cache_index = cache_index
        self.policy = policy

    def run(self, plan: FallbackDryRunPlan) -> FallbackDryRunResult:
        if not self.cache_index:
             return self._build_failed(plan, "No cache index provided.")

        eval_res = evaluate_fallback_chain(plan, self.cache_index)

        status = FallbackDryRunStatus.UNKNOWN
        decision = FallbackDryRunDecision.UNKNOWN

        cache_hit = False
        cache_miss = False
        selected = eval_res["selected_provider"]

        if selected:
            cache_hit = True
            if selected == plan.primary_provider:
                status = FallbackDryRunStatus.CACHE_HIT_PRIMARY
                decision = FallbackDryRunDecision.USE_PRIMARY_CACHE
            else:
                status = FallbackDryRunStatus.FALLBACK_SELECTED
                decision = FallbackDryRunDecision.USE_FALLBACK_CACHE
        else:
            cache_miss = True
            status = FallbackDryRunStatus.FALLBACK_EXHAUSTED
            decision = FallbackDryRunDecision.REQUEST_FUTURE_REFRESH

        risk_flags = []
        if cache_miss:
            risk_flags.append(ProviderCacheRiskFlag.FALLBACK_EXHAUSTED)

        return FallbackDryRunResult(
            result_id=create_fallback_dry_run_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            plan_id=plan.plan_id,
            status=status,
            decision=decision,
            selected_provider=selected,
            selected_cache_record_id=eval_res["selected_record_id"],
            attempted_providers=eval_res["attempted"],
            skipped_providers=eval_res["skipped"],
            fallback_exhausted=eval_res["exhausted"],
            cache_hit=cache_hit,
            cache_miss=cache_miss,
            stale_used=eval_res["stale_used"],
            source_comparison_required=cache_hit and selected != plan.primary_provider, # heuristic
            dry_run_only=True,
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
            risk_flags=risk_flags,
            warnings=[],
            errors=[],
            metadata={}
        )

    def _build_failed(self, plan: FallbackDryRunPlan, error: str) -> FallbackDryRunResult:
        return FallbackDryRunResult(
            result_id=create_fallback_dry_run_result_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            plan_id=plan.plan_id,
            status=FallbackDryRunStatus.FAILED,
            decision=FallbackDryRunDecision.BLOCK,
            selected_provider=None, selected_cache_record_id=None,
            attempted_providers=[], skipped_providers=[], fallback_exhausted=True,
            cache_hit=False, cache_miss=True, stale_used=False, source_comparison_required=False,
            dry_run_only=True, network_used=False, paid_api_used=False, scraping_used=False, html_parsing_used=False,
            broker_used=False, order_created=False, paper_state_mutated=False, telegram_real_sent=False, dashboard_started=False,
            passed=False, risk_flags=[], warnings=[], errors=[error], metadata={}
        )

    def run_batch(self, plans: list[FallbackDryRunPlan]) -> list[FallbackDryRunResult]:
        return [self.run(p) for p in plans]

    def validate_result_safety(self, result: FallbackDryRunResult) -> list[str]:
        errors = []
        if result.network_used: errors.append("network_used is true")
        if result.paid_api_used: errors.append("paid_api_used is true")
        if result.broker_used: errors.append("broker_used is true")
        if result.order_created: errors.append("order_created is true")
        if result.paper_state_mutated: errors.append("paper_state_mutated is true")
        if result.telegram_real_sent: errors.append("telegram_real_sent is true")
        if result.dashboard_started: errors.append("dashboard_started is true")
        if not result.dry_run_only: errors.append("dry_run_only is false")
        return errors

    def summary(self, results: list[FallbackDryRunResult]) -> dict[str, Any]:
        return {"total": len(results), "hits": sum(1 for r in results if r.cache_hit)}
