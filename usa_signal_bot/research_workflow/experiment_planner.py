from typing import Any, List, Optional, Tuple
import datetime
from .workflow_models import ExperimentPlan, ResearchHypothesis, RepairQueueItem, ParameterChangeProposal, AcceptanceGate, create_experiment_plan_id
from .parameter_change_proposals import parameter_change_from_repair_item, create_parameter_change_proposal
from .validation_plan import build_default_validation_plan
from .acceptance_gates import default_acceptance_gates_for_experiment
from .rollback_plan import build_default_rollback_plan
from .experiment_scope import classify_experiment_type_from_repair_item, experiment_scope_risk_level
from ..core.enums import ExperimentType, ExperimentScope, ExperimentStatus, ResearchRiskLevel

class ControlledExperimentPlanner:
    def __init__(self, require_manual_review: bool = True, allow_auto_execution: bool = False):
        self.require_manual_review = require_manual_review
        self.allow_auto_execution = allow_auto_execution

    def plan_experiment_for_hypothesis(self, hypothesis: ResearchHypothesis, repair_item: Optional[RepairQueueItem] = None) -> ExperimentPlan:
        experiment_type = ExperimentType.BASELINE_COMPARISON
        if repair_item:
            experiment_type = classify_experiment_type_from_repair_item(repair_item)

        proposals = self.build_parameter_proposals(hypothesis, repair_item)
        val_plan = self.build_validation_plan(hypothesis, experiment_type, hypothesis.target_scope)
        gates = self.build_acceptance_gates(experiment_type, hypothesis.target_scope)
        rollback = self.build_rollback_plan(hypothesis)
        risk = self.determine_experiment_risk_level(hypothesis, repair_item)

        return ExperimentPlan(
            experiment_id=create_experiment_plan_id(),
            created_at_utc=datetime.datetime.utcnow().isoformat() + "Z",
            experiment_type=experiment_type,
            scope=hypothesis.target_scope,
            status=ExperimentStatus.DRAFT,
            title=f"Experiment for {hypothesis.title}",
            description=f"Testing hypothesis: {hypothesis.hypothesis_statement}",
            linked_hypothesis_id=hypothesis.hypothesis_id,
            baseline_config_ref="current_main",
            candidate_config_ref="candidate_branch",
            parameter_change_proposals=proposals,
            validation_plan=val_plan,
            acceptance_gates=gates,
            rollback_plan=rollback,
            dependency_ids=[],
            risk_level=risk,
            allowed_for_auto_execution=self.allow_auto_execution,
            warnings=[],
            errors=[],
            metadata={}
        )

    def plan_experiments_for_hypotheses(self, hypotheses: List[ResearchHypothesis], repair_items: Optional[List[RepairQueueItem]] = None) -> List[ExperimentPlan]:
        plans = []
        item_map = {item.item_id: item for item in (repair_items or [])}
        for h in hypotheses:
            linked_item = None
            if h.linked_repair_item_ids and h.linked_repair_item_ids[0] in item_map:
                linked_item = item_map[h.linked_repair_item_ids[0]]
            plans.append(self.plan_experiment_for_hypothesis(h, linked_item))
        return plans

    def build_baseline_candidate_refs(self, hypothesis: ResearchHypothesis) -> Tuple[Optional[str], Optional[str]]:
        return ("current_main", "candidate_branch")

    def build_parameter_proposals(self, hypothesis: ResearchHypothesis, repair_item: Optional[RepairQueueItem] = None) -> List[ParameterChangeProposal]:
        if repair_item:
            return parameter_change_from_repair_item(repair_item)
        return []

    def build_validation_plan(self, hypothesis: ResearchHypothesis, experiment_type: ExperimentType, scope: ExperimentScope) -> dict[str, Any]:
        return build_default_validation_plan(scope, experiment_type)

    def build_acceptance_gates(self, experiment_type: ExperimentType, scope: ExperimentScope) -> List[AcceptanceGate]:
        return default_acceptance_gates_for_experiment(experiment_type, scope)

    def build_rollback_plan(self, hypothesis: ResearchHypothesis) -> dict[str, Any]:
        return build_default_rollback_plan()

    def determine_experiment_risk_level(self, hypothesis: ResearchHypothesis, repair_item: Optional[RepairQueueItem] = None) -> ResearchRiskLevel:
        priority = repair_item.priority if repair_item else None
        return experiment_scope_risk_level(hypothesis.target_scope, priority)
