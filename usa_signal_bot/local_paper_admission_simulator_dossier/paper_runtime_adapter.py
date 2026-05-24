from typing import Any
from usa_signal_bot.local_paper_admission_simulator_dossier.simulator_dossier_models import SimulatorDossierFullReview

def build_read_only_paper_snapshot_for_simulator_dossier(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "snapshot_type": "READ_ONLY_PAPER_SNAPSHOT",
        "paper_payload": paper_payload or {},
        "paper_state_committed": False,
        "paper_order_executed": False,
        "portfolio_state_mutated": False
    }

def build_sandbox_runtime_admission_blocker_snapshot(paper_payload: dict[str, Any] | None = None) -> dict[str, Any]:
    return {
        "snapshot_type": "SANDBOX_RUNTIME_ADMISSION_BLOCKER_SNAPSHOT",
        "paper_payload": paper_payload or {},
        "sandbox_runtime_admission_allowed": False,
        "paper_sandbox_runtime_allowed": False
    }

def compare_simulator_dossier_to_paper_snapshot(review: SimulatorDossierFullReview, paper_snapshot: dict[str, Any]) -> dict[str, Any]:
    mutations = []
    if paper_snapshot.get("paper_state_committed"): mutations.append("paper_state_committed")
    if paper_snapshot.get("paper_order_executed"): mutations.append("paper_order_executed")
    if paper_snapshot.get("portfolio_state_mutated"): mutations.append("portfolio_state_mutated")
    return {
        "mutations_found": len(mutations) > 0,
        "mutations": mutations
    }

def validate_paper_runtime_not_mutated_by_simulator_dossier(before: dict[str, Any], after: dict[str, Any]) -> list[str]:
    errors = []
    if not before.get("paper_state_committed") and after.get("paper_state_committed"):
        errors.append("paper_state_committed changed to True")
    if not before.get("portfolio_state_mutated") and after.get("portfolio_state_mutated"):
        errors.append("portfolio_state_mutated changed to True")
    return errors

def attach_simulator_dossier_metadata_to_paper_analytics(payload: dict[str, Any], review: SimulatorDossierFullReview) -> dict[str, Any]:
    output = payload.copy()
    output["simulator_dossier_review_id"] = review.review_id
    output["simulator_dossier_status"] = review.dossiers[0].status.value if review.dossiers else "UNKNOWN"
    return output

def paper_runtime_simulator_dossier_adapter_to_text(payload: dict[str, Any]) -> str:
    return "--- Paper Runtime Simulator Dossier Adapter ---\n" + str(payload)
