"""System Acceptance Evaluator."""

from typing import Any, Dict, List, Optional
from pathlib import Path
from datetime import datetime, timezone
import logging

from usa_signal_bot.core.enums import AcceptanceScope, AcceptanceDecision, ReadinessGateStatus
from usa_signal_bot.quality.quality_models import (
    ResearchQualityScorecard,
    ProductionReadinessGateResult,
    SystemAcceptanceResult,
    create_acceptance_id,
)
from usa_signal_bot.quality.artifact_collectors import load_latest_quality_artifacts
from usa_signal_bot.quality.scorecard import build_research_quality_scorecard
from usa_signal_bot.quality.readiness_gate import ProductionReadinessGate

logger = logging.getLogger(__name__)

class SystemAcceptanceEvaluator:
    def __init__(self, data_root: Path, project_root: Optional[Path] = None, scope: AcceptanceScope = AcceptanceScope.FULL_LOCAL_STACK):
        self.data_root = data_root
        self.project_root = project_root or Path.cwd()
        self.scope = scope

    def collect_artifacts(self) -> Dict[str, Any]:
        return load_latest_quality_artifacts(self.data_root)

    def build_scorecard(self, artifacts: Dict[str, Any]) -> ResearchQualityScorecard:
        artifacts["data_root"] = str(self.project_root)
        return build_research_quality_scorecard(artifacts)

    def run_gate(self, scorecard: ResearchQualityScorecard, artifacts: Dict[str, Any]) -> ProductionReadinessGateResult:
        gate = ProductionReadinessGate(scope=self.scope)
        return gate.evaluate(scorecard, artifacts)

    def decide_acceptance(self, scorecard: ResearchQualityScorecard, gate_result: ProductionReadinessGateResult) -> AcceptanceDecision:
        if gate_result.status == ReadinessGateStatus.BLOCKED:
            return AcceptanceDecision.BLOCKED
        if gate_result.status == ReadinessGateStatus.INSUFFICIENT_DATA:
            return AcceptanceDecision.INSUFFICIENT_DATA
        if gate_result.status == ReadinessGateStatus.FAILED:
            return AcceptanceDecision.NOT_ACCEPTED
        if gate_result.status == ReadinessGateStatus.WARNING:
            return AcceptanceDecision.ACCEPTED_WITH_WARNINGS
        return AcceptanceDecision.ACCEPTED_FOR_LOCAL_RESEARCH

    def build_required_actions(self, scorecard: ResearchQualityScorecard, gate_result: ProductionReadinessGateResult) -> List[str]:
        actions = []
        if gate_result.status in (ReadinessGateStatus.FAILED, ReadinessGateStatus.BLOCKED):
            for e in gate_result.errors:
                actions.append(f"Resolve gate failure: {e}")
        return actions

    def build_optional_actions(self, scorecard: ResearchQualityScorecard, gate_result: ProductionReadinessGateResult) -> List[str]:
        actions = []
        for w in gate_result.warnings:
            actions.append(f"Consider resolving warning: {w}")
        return actions

    def run(self) -> SystemAcceptanceResult:
        logger.info(f"Starting System Acceptance Evaluation. Scope: {self.scope.name}")

        artifacts = self.collect_artifacts()
        scorecard = self.build_scorecard(artifacts)
        gate_result = self.run_gate(scorecard, artifacts)

        decision = self.decide_acceptance(scorecard, gate_result)
        required_actions = self.build_required_actions(scorecard, gate_result)
        optional_actions = self.build_optional_actions(scorecard, gate_result)

        summary = f"System evaluated to {decision.name}. Score: {scorecard.overall_score}"

        return SystemAcceptanceResult(
            acceptance_id=create_acceptance_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            scope=self.scope,
            decision=decision,
            scorecard=scorecard,
            gate_result=gate_result,
            acceptance_summary=summary,
            required_actions=required_actions,
            optional_actions=optional_actions,
            output_paths={},
            warnings=gate_result.warnings,
            errors=gate_result.errors
        )
