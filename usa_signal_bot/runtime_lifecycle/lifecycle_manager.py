from typing import Dict, Any, Optional, List
from usa_signal_bot.runtime_lifecycle.phase104_models import (
    RuntimeLifecycleContext,
    StartupCheckReport,
    ServiceReadinessMatrix,
    ReadinessGate,
    create_runtime_lifecycle_context_id,
    _now_str
)
from usa_signal_bot.core.enums import RuntimeLifecycleStatus, RuntimeLifecycleDecision
from usa_signal_bot.runtime_lifecycle.lifecycle_state_machine import RuntimeLifecycleStateMachine
from usa_signal_bot.runtime_lifecycle.startup_check_runner import StartupCheckRunner
from usa_signal_bot.runtime_lifecycle.service_readiness_matrix import build_service_readiness_matrix
from usa_signal_bot.runtime_lifecycle.readiness_gate_builder import build_readiness_gate
from usa_signal_bot.runtime_lifecycle.readiness_gate_evaluator import evaluate_readiness_gate
from usa_signal_bot.runtime_lifecycle.lifecycle_dry_run_validator import lifecycle_dry_run_passed, validate_lifecycle_dry_run
from usa_signal_bot.core.exceptions import LifecycleManagerError

class RuntimeLifecycleManager:
    def __init__(self, service_graph_payload: Optional[Dict[str, Any]] = None, config: Optional[Dict[str, Any]] = None):
        self.service_graph_payload = service_graph_payload
        self.config = config or {}
        self.state_machine = RuntimeLifecycleStateMachine()
        self.startup_runner = StartupCheckRunner()

    def run_startup_checks(self) -> StartupCheckReport:
        self.state_machine.transition(RuntimeLifecycleStatus.CREATED, "Begin startup checks")
        report = self.startup_runner.run_all_checks()
        if report.startup_checks_passed:
            self.state_machine.transition(RuntimeLifecycleStatus.CONFIG_CHECKED, "Startup checks passed")
        else:
            self.state_machine.transition(RuntimeLifecycleStatus.BLOCKED, "Startup checks failed")
        return report

    def build_readiness_matrix(self) -> ServiceReadinessMatrix:
        self.state_machine.transition(RuntimeLifecycleStatus.DEPENDENCIES_CHECKED, "Building readiness matrix")
        return build_service_readiness_matrix(self.service_graph_payload)

    def build_readiness_gate(self, startup_report: StartupCheckReport, matrix: ServiceReadinessMatrix) -> ReadinessGate:
        self.state_machine.transition(RuntimeLifecycleStatus.READINESS_CHECKED, "Evaluating readiness gate")
        gate = build_readiness_gate(startup_report, matrix)
        decision = evaluate_readiness_gate(gate)
        gate.decision = decision
        return gate

    def run_lifecycle_dry_run(self) -> RuntimeLifecycleContext:
        try:
            report = self.run_startup_checks()
            matrix = self.build_readiness_matrix()
            gate = self.build_readiness_gate(report, matrix)

            if gate.gate_passed:
                self.state_machine.transition(RuntimeLifecycleStatus.DRY_RUN_VALIDATED, "Dry run validated")
                self.state_machine.transition(RuntimeLifecycleStatus.READY_FOR_FUTURE_PHASE, "Ready for Phase 105")
                decision = RuntimeLifecycleDecision.READY_FOR_PHASE105_REVIEW
            else:
                decision = RuntimeLifecycleDecision.BLOCK

            ctx = RuntimeLifecycleContext(
                context_id=create_runtime_lifecycle_context_id(),
                created_at_utc=_now_str(),
                status=self.state_machine.current_status(),
                decision=decision,
                source_service_graph_ingestion_id=None,
                startup_report=report,
                readiness_matrix=matrix,
                readiness_gate=gate,
                transitions=self.state_machine.history(),
                lifecycle_ready=gate.gate_passed,
                ready_for_phase105=gate.gate_passed,
                activation_allowed=False,
                active_paper_enabled=False,
                broker_execution_enabled=False,
                paper_state_mutation_enabled=False,
                telegram_real_send_enabled=False,
                scraping_enabled=False,
                dashboard_enabled=False,
                execution_performed=False,
                network_used=False,
                broker_used=False,
                order_created=False,
                paper_state_mutated=False,
                telegram_real_sent=False,
                scraping_used=False,
                dashboard_started=False,
                risk_flags=gate.risk_flags,
                warnings=gate.warnings,
                errors=gate.errors,
                metadata={}
            )

            dry_run_errors = validate_lifecycle_dry_run(ctx)
            if dry_run_errors:
                raise LifecycleManagerError(f"Dry run safety violation: {dry_run_errors}")

            return ctx

        except Exception as e:
            self.state_machine.transition(RuntimeLifecycleStatus.FAILED, f"Error: {str(e)}")
            raise LifecycleManagerError(f"Failed to run lifecycle manager: {str(e)}")

    def validate_lifecycle_safety(self, context: RuntimeLifecycleContext) -> List[str]:
        return validate_lifecycle_dry_run(context)

    def lifecycle_summary(self, context: RuntimeLifecycleContext) -> Dict[str, Any]:
        return {
            "status": context.status.value,
            "decision": context.decision.value,
            "ready_for_phase105": context.ready_for_phase105
        }
