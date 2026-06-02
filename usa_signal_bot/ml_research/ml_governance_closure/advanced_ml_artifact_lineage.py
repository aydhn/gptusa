from typing import Any
import hashlib
import json

from usa_signal_bot.ml_research.ml_governance_closure.phase145_models import (
    AdvancedMLArtifactLineage,
    AdvancedMLLineageNode,
    AdvancedMLLineageNodeKind,
    create_advanced_ml_artifact_lineage_id,
    create_advanced_ml_lineage_node_id,
    current_time
)

def build_lineage_node_from_phase_review(phase_number: int, payload: dict[str, Any]) -> AdvancedMLLineageNode:
    return AdvancedMLLineageNode(
        node_id=create_advanced_ml_lineage_node_id(),
        created_at_utc=current_time(),
        node_kind=AdvancedMLLineageNodeKind.PHASE_REVIEW,
        phase_number=phase_number,
        artifact_name=f"Phase {phase_number} Review",
        artifact_id=payload.get("review_id"),
        source_path=None,
        source_hash=None,
        available=True,
        validated=True,
        research_data_only=True,
        non_activation=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def compute_advanced_ml_artifact_lineage_hash(lineage: AdvancedMLArtifactLineage) -> str:
    components = [n.node_id for n in lineage.nodes]
    content_str = json.dumps(components, sort_keys=True)
    return hashlib.sha256(content_str.encode("utf-8")).hexdigest()

def build_advanced_ml_artifact_lineage(
    phase_reviews: list[dict[str, Any]],
    extra_artifacts: list[dict[str, Any]] | None = None
) -> AdvancedMLArtifactLineage:

    nodes = []
    phase_numbers_covered = []

    for review in phase_reviews:
        phase_num = review.get("phase_number")
        if phase_num is not None:
            nodes.append(build_lineage_node_from_phase_review(phase_num, review))
            phase_numbers_covered.append(phase_num)

    # Check if Phase 136-145 coverage is complete
    required_phases = list(range(136, 146))
    missing_phase_numbers = [p for p in required_phases if p not in phase_numbers_covered]

    lineage = AdvancedMLArtifactLineage(
        lineage_id=create_advanced_ml_artifact_lineage_id(),
        created_at_utc=current_time(),
        nodes=nodes,
        phase_numbers_covered=sorted(phase_numbers_covered),
        missing_phase_numbers=missing_phase_numbers,
        lineage_hash=None, # Computed below
        lineage_complete=len(missing_phase_numbers) == 0,
        lineage_valid=True,
        research_data_only=True,
        non_activation=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    if missing_phase_numbers:
        lineage.warnings.append(f"Missing phase numbers: {missing_phase_numbers}")
        lineage.lineage_complete = False

    lineage.lineage_hash = compute_advanced_ml_artifact_lineage_hash(lineage)
    return lineage

def validate_advanced_ml_artifact_lineage(lineage: AdvancedMLArtifactLineage) -> list[str]:
    errors = []
    if not lineage.research_data_only or not lineage.non_activation:
        errors.append("Lineage must be non_activation and research_data_only")
    if not lineage.lineage_complete:
        errors.append(f"Lineage incomplete. Missing phases: {lineage.missing_phase_numbers}")
    return errors

def advanced_ml_artifact_lineage_summary(lineage: AdvancedMLArtifactLineage) -> dict[str, Any]:
    return {
        "node_count": len(lineage.nodes),
        "phases_covered": lineage.phase_numbers_covered,
        "missing_phases": lineage.missing_phase_numbers,
        "complete": lineage.lineage_complete
    }

def advanced_ml_artifact_lineage_to_text(lineage: AdvancedMLArtifactLineage, limit: int = 300) -> str:
    summary = advanced_ml_artifact_lineage_summary(lineage)
    return f"Artifact lineage built. Nodes: {summary['node_count']}. Complete: {summary['complete']}. Missing: {summary['missing_phases']}"
