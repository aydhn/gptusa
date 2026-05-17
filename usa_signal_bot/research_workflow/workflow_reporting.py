from typing import Any
from .workflow_models import (
    RepairQueueItem, ResearchHypothesis, ParameterChangeProposal,
    AcceptanceGate, ExperimentPlan, ResearchDecisionLogEntry,
    ResearchWorkflowReview
)
from .repair_queue import repair_queue_to_text
from .hypothesis_tracker import hypothesis_tracker_to_text
from .parameter_change_proposals import parameter_change_proposals_to_text
from .acceptance_gates import acceptance_gates_to_text

def repair_queue_item_to_text(item: RepairQueueItem) -> str:
    return repair_queue_to_text([item])

def research_hypothesis_to_text(item: ResearchHypothesis) -> str:
    return hypothesis_tracker_to_text([item])

def parameter_change_proposal_to_text(item: ParameterChangeProposal) -> str:
    return parameter_change_proposals_to_text([item])

def acceptance_gate_to_text(item: AcceptanceGate) -> str:
    return acceptance_gates_to_text([item])

def experiment_plan_to_text(item: ExperimentPlan) -> str:
    lines = [f"Experiment Plan: {item.title}"]
    lines.append(f"  Scope: {item.scope.value}")
    lines.append(f"  Type: {item.experiment_type.value}")
    lines.append(f"  Status: {item.status.value}")
    lines.append(f"  Risk: {item.risk_level.value}")
    lines.append(f"  Proposals: {len(item.parameter_change_proposals)}")
    lines.append(f"  Gates: {len(item.acceptance_gates)}")
    return "\n".join(lines)

def research_decision_log_entry_to_text(item: ResearchDecisionLogEntry) -> str:
    return f"Decision [{item.entity_type} {item.entity_id}]: {item.decision} - {item.rationale}"

def research_workflow_review_to_text(item: ResearchWorkflowReview, limit: int = 100) -> str:
    lines = [
        f"Research Workflow Review: {item.review_id}",
        f"Report Type: {item.report_type.value}",
        f"Repair Items: {len(item.repair_items)}",
        f"Hypotheses: {len(item.hypotheses)}",
        f"Experiment Plans: {len(item.experiment_plans)}",
        f"Decision Logs: {len(item.decision_log_entries)}",
        ""
    ]
    lines.append(research_workflow_limitations_text())
    return "\n".join(lines)

def workflow_store_summary_to_text(summary: dict[str, Any]) -> str:
    return f"Workflow Store: {summary['review_count']} total reviews. Latest: {summary['latest_review']}"

def research_workflow_limitations_text() -> str:
    return (
        "*** RESEARCH WORKFLOW LIMITATIONS ***\n"
        "1. This is a local research metadata system.\n"
        "2. It is NOT an auto-optimizer.\n"
        "3. It does NOT automatically change parameters in production.\n"
        "4. Experiment plans do NOT run real backtests autonomously.\n"
        "5. A PASS in an acceptance gate is NOT a live trading approval.\n"
        "6. A supported hypothesis is NOT a guarantee of future performance.\n"
        "7. NO live, paper, or demo broker orders will be generated.\n"
        "8. This is NOT investment advice."
    )
