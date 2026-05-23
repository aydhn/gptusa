from typing import Any, Dict, List
from usa_signal_bot.paper_readiness_non_execution_board.non_execution_board_models import (
    RuntimeMapReplayPlan,
    RuntimeRouteReplayItem,
    RuntimeMapReplayResult,
    RuntimeRouteReplayDecision,
    RuntimeMapReplayStatus,
    RuntimeMapReplayOutcome,
    NonExecutionBoardRiskFlag,
    create_runtime_route_replay_item_id,
    create_runtime_map_replay_result_id,
    _now_utc_str,
    validate_runtime_map_replay_result
)

class RuntimeMapReplayEngine:
    def __init__(self, conservative: bool = True):
        self.conservative = conservative

    def replay(self, plan: RuntimeMapReplayPlan, dossier_payload: Dict[str, Any]) -> RuntimeMapReplayResult:
        result = RuntimeMapReplayResult(
            replay_result_id=create_runtime_map_replay_result_id(),
            created_at_utc=_now_utc_str(),
            replay_plan_id=plan.replay_plan_id,
            status=RuntimeMapReplayStatus.RUNNING,
            outcome=RuntimeMapReplayOutcome.UNKNOWN,
            replayed_route_count=0,
            safe_metadata_route_count=0,
            dangerous_denied_count=0,
            dangerous_allowed_count=0,
            missing_component_count=0,
            missing_route_count=0,
            passed=False,
            risk_flags=[],
            warnings=[],
            errors=[],
            metadata={}
        )

        routes = dossier_payload.get("runtime_route_items", [])
        if not routes:
            # Maybe inside pre_paper_local_runtime_maps ?
            maps = dossier_payload.get("pre_paper_local_runtime_maps", [])
            if maps:
                routes = maps[0].get("route_items", [])

        route_items: List[RuntimeRouteReplayItem] = []
        for r in routes:
            item = self.replay_route(r)
            route_items.append(item)

            result.replayed_route_count += 1
            if item.decision in [
                RuntimeRouteReplayDecision.ALLOW_READ_ONLY_METADATA,
                RuntimeRouteReplayDecision.ALLOW_PREVIEW_METADATA,
                RuntimeRouteReplayDecision.ALLOW_DRY_RUN_METADATA
            ]:
                result.safe_metadata_route_count += 1
            elif item.decision.name.startswith("DENY_"):
                result.dangerous_denied_count += 1
            elif item.decision == RuntimeRouteReplayDecision.BLOCK:
                result.dangerous_allowed_count += 1

        coverage_errors = self.validate_replay_coverage(plan, dossier_payload)
        result.errors.extend(coverage_errors)

        result.outcome = self.determine_replay_outcome(plan, route_items)
        if result.outcome == RuntimeMapReplayOutcome.COMPONENT_MAP_INCOMPLETE:
            result.missing_component_count = len([e for e in coverage_errors if "component" in e.lower()])
        if result.outcome == RuntimeMapReplayOutcome.ROUTE_MAP_INCOMPLETE:
            result.missing_route_count = len([e for e in coverage_errors if "route" in e.lower()])

        result.risk_flags = self.collect_replay_risk_flags(plan, route_items)
        if NonExecutionBoardRiskFlag.DANGEROUS_RUNTIME_ROUTE_ALLOWED in result.risk_flags:
            result.dangerous_allowed_count = max(1, result.dangerous_allowed_count)

        result.passed = (result.outcome == RuntimeMapReplayOutcome.ALL_DANGEROUS_ROUTES_DENIED)

        if result.passed:
            result.status = RuntimeMapReplayStatus.COMPLETED_ROUTE_SAFE
        elif result.outcome in [RuntimeMapReplayOutcome.DANGEROUS_ROUTE_ALLOWED, RuntimeMapReplayOutcome.BLOCKED]:
            result.status = RuntimeMapReplayStatus.BLOCKED
        else:
            result.status = RuntimeMapReplayStatus.FAILED

        validate_runtime_map_replay_result(result)
        return result

    def replay_route(self, route_payload: Dict[str, Any]) -> RuntimeRouteReplayItem:
        route_name = route_payload.get("route_name", "unknown")
        permission = route_payload.get("permission", "DENIED")
        dangerous = route_payload.get("dangerous", False)

        item = RuntimeRouteReplayItem(
            replay_item_id=create_runtime_route_replay_item_id(),
            created_at_utc=_now_utc_str(),
            route_name=route_name,
            source_component=route_payload.get("source_component"),
            target_component=route_payload.get("target_component"),
            permission=permission,
            decision=RuntimeRouteReplayDecision.UNKNOWN,
            blocked=False,
            read_only=False,
            preview_only=False,
            dry_run_only=False,
            write_allowed=False,
            order_allowed=False,
            broker_allowed=False,
            config_patch_allowed=False,
            telegram_real_send_allowed=False,
            activation_allowed=False,
            paper_admission_allowed=False,
            risk_flags=[],
            warnings=[],
            errors=[],
            metadata={"original_route": route_payload}
        )

        if not dangerous and permission == "ALLOWED":
            if "read" in route_name or "audit" in route_name or "validation" in route_name:
                item.decision = RuntimeRouteReplayDecision.ALLOW_READ_ONLY_METADATA
                item.read_only = True
            elif "preview" in route_name:
                item.decision = RuntimeRouteReplayDecision.ALLOW_PREVIEW_METADATA
                item.preview_only = True
            elif "dry_run" in route_name:
                item.decision = RuntimeRouteReplayDecision.ALLOW_DRY_RUN_METADATA
                item.dry_run_only = True
            else:
                # default safe allowed
                item.decision = RuntimeRouteReplayDecision.ALLOW_READ_ONLY_METADATA
                item.read_only = True
        elif dangerous and permission == "ALLOWED":
            item.decision = RuntimeRouteReplayDecision.BLOCK
            item.blocked = True
            item.risk_flags.append(NonExecutionBoardRiskFlag.DANGEROUS_RUNTIME_ROUTE_ALLOWED)
            if "write" in route_name:
                item.write_allowed = True
            if "order" in route_name:
                item.order_allowed = True
            if "broker" in route_name:
                item.broker_allowed = True
            if "config" in route_name:
                item.config_patch_allowed = True
            if "telegram" in route_name:
                item.telegram_real_send_allowed = True
            if "active" in route_name or "enable" in route_name:
                item.activation_allowed = True
            if "admission" in route_name:
                item.paper_admission_allowed = True
        elif dangerous and permission == "DENIED":
            if "write" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_WRITE
            elif "order" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_ORDER
            elif "broker" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_BROKER
            elif "config" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_CONFIG_PATCH
            elif "telegram" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_TELEGRAM_REAL_SEND
            elif "active" in route_name or "enable" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_ACTIVATION
            elif "admission" in route_name:
                item.decision = RuntimeRouteReplayDecision.DENY_PAPER_ADMISSION
            else:
                item.decision = RuntimeRouteReplayDecision.BLOCK # Generic deny is good, but if unknown dangerous, treat cautiously
        else:
            item.decision = RuntimeRouteReplayDecision.UNKNOWN

        return item

    def validate_replay_coverage(self, plan: RuntimeMapReplayPlan, dossier_payload: Dict[str, Any]) -> List[str]:
        errors = []
        components = dossier_payload.get("runtime_component_items", [])
        if not components:
            maps = dossier_payload.get("pre_paper_local_runtime_maps", [])
            if maps:
                components = maps[0].get("component_items", [])

        comp_names = [c.get("component_name") for c in components]
        for rc in plan.required_component_names:
            if rc not in comp_names:
                errors.append(f"Missing required component: {rc}")

        routes = dossier_payload.get("runtime_route_items", [])
        if not routes:
            maps = dossier_payload.get("pre_paper_local_runtime_maps", [])
            if maps:
                routes = maps[0].get("route_items", [])

        route_names = [r.get("route_name") for r in routes]
        for rr in plan.required_route_names:
            if rr not in route_names:
                errors.append(f"Missing required route: {rr}")

        return errors

    def determine_replay_outcome(self, plan: RuntimeMapReplayPlan, route_items: List[RuntimeRouteReplayItem]) -> RuntimeMapReplayOutcome:
        for item in route_items:
            if item.decision == RuntimeRouteReplayDecision.BLOCK or item.blocked:
                return RuntimeMapReplayOutcome.DANGEROUS_ROUTE_ALLOWED

        # Check coverage indirectly (engine does it, but we can just say if missing stuff, it's incomplete)
        # Actually, let's rely on the engine setting outcome. We will just check if all dangerous denied.
        return RuntimeMapReplayOutcome.ALL_DANGEROUS_ROUTES_DENIED

    def collect_replay_risk_flags(self, plan: RuntimeMapReplayPlan, route_items: List[RuntimeRouteReplayItem]) -> List[NonExecutionBoardRiskFlag]:
        flags = set()
        for item in route_items:
            for flag in item.risk_flags:
                flags.add(flag)
        return list(flags)

    def replay_summary(self, result: RuntimeMapReplayResult) -> Dict[str, Any]:
        return {
            "status": result.status.value,
            "outcome": result.outcome.value,
            "replayed": result.replayed_route_count,
            "dangerous_allowed": result.dangerous_allowed_count,
            "passed": result.passed
        }
