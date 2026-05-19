from typing import Any, Dict, List
from usa_signal_bot.core.enums import FrozenArtifactSource, ReleaseBundleType

def collect_artifacts_from_governance_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [payload] if payload else []

def collect_artifacts_from_release_candidate_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [payload] if payload else []

def collect_artifacts_from_execution_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [payload] if payload else []

def normalize_artifact_payload(payload: Dict[str, Any], source: FrozenArtifactSource) -> Dict[str, Any]:
    return {"source": source.value, "payload": payload}

def required_bundle_artifact_types(bundle_type: ReleaseBundleType) -> List[str]:
    return ["release_candidate", "governance_review", "evidence_pack", "comparison_report", "acceptance_gate_evaluation", "config_snapshot", "validation_report", "safety_report"]

def artifact_collection_summary(artifacts: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"collected_count": len(artifacts)}

def artifact_collector_to_text(payload: Dict[str, Any]) -> str:
    return f"Artifact Collector summary: {payload}"
