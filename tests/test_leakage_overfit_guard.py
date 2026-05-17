
from usa_signal_bot.research_workflow.leakage_overfit_guard import leakage_risk_warnings
from usa_signal_bot.research_workflow.workflow_models import ExperimentPlan, create_experiment_plan_id
from usa_signal_bot.core.enums import ExperimentType, ExperimentScope, ExperimentStatus, ResearchRiskLevel
import datetime

def test_leakage_guard():
    plan = ExperimentPlan(
        experiment_id=create_experiment_plan_id(), created_at_utc=datetime.datetime.utcnow().isoformat(),
        experiment_type=ExperimentType.PARAMETER_CHANGE, scope=ExperimentScope.SINGLE_STRATEGY,
        status=ExperimentStatus.DRAFT, title="T1", description="D1", linked_hypothesis_id=None,
        baseline_config_ref=None, candidate_config_ref=None, parameter_change_proposals=[],
        validation_plan={}, acceptance_gates=[], rollback_plan={}, dependency_ids=[],
        risk_level=ResearchRiskLevel.LOW, allowed_for_auto_execution=False, warnings=[], errors=[], metadata={}
    )
    warnings = leakage_risk_warnings(plan)
    assert len(warnings) > 0
