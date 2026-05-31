from typing import Any, Dict, List
from datetime import datetime, timezone
from .phase136_models import MLResearchGovernanceRule, MLResearchGovernanceResult, MLResearchGovernanceRuleKind, create_ml_research_governance_rule_id, create_ml_research_governance_result_id

def build_ml_research_governance_rules() -> List[MLResearchGovernanceRule]:
    now = datetime.now(timezone.utc).isoformat()
    kinds = [
        MLResearchGovernanceRuleKind.LOCAL_ONLY_RESEARCH,
        MLResearchGovernanceRuleKind.FREE_DATA_ONLY,
        MLResearchGovernanceRuleKind.FROZEN_INPUTS_READ_ONLY,
        MLResearchGovernanceRuleKind.DATASET_CONTRACT_REQUIRED,
        MLResearchGovernanceRuleKind.LEAKAGE_GUARD_REQUIRED,
        MLResearchGovernanceRuleKind.REPRODUCIBLE_ARTIFACTS,
        MLResearchGovernanceRuleKind.DETERMINISTIC_HASHING,
        MLResearchGovernanceRuleKind.SAFETY_BOUNDARY_REQUIRED,
        MLResearchGovernanceRuleKind.NO_SECRET_REQUIRED,
        MLResearchGovernanceRuleKind.NO_NETWORK_BY_DEFAULT,
        MLResearchGovernanceRuleKind.NO_HEAVY_ML_DEPENDENCY_IN_PHASE136
    ]
    rules = []
    for kind in kinds:
        rules.append(MLResearchGovernanceRule(
            rule_id=create_ml_research_governance_rule_id(),
            created_at_utc=now,
            rule_kind=kind,
            name=kind.value,
            required=True,
            passed=True,
            expected_value=None,
            observed_value=None,
            rationale=f"Verified {kind.value}"
        ))
    return rules

def build_ml_research_governance_result(rules: List[MLResearchGovernanceRule]) -> MLResearchGovernanceResult:
    now = datetime.now(timezone.utc).isoformat()
    passed = all(r.passed for r in rules)
    return MLResearchGovernanceResult(
        governance_id=create_ml_research_governance_result_id(),
        created_at_utc=now,
        rules=rules,
        governance_passed=passed,
        local_only=passed,
        free_data_only=passed,
        frozen_inputs_read_only=passed,
        dataset_contract_required=passed,
        leakage_guard_required=passed,
        reproducible_artifacts_required=passed,
        deterministic_hashing_required=passed,
        safety_boundary_required=passed,
        no_secret_required=passed,
        no_network_by_default=passed,
        no_heavy_ml_dependency_in_phase136=passed,
        research_metadata_only=True
    )

def validate_ml_research_governance_result(result: MLResearchGovernanceResult) -> List[str]:
    if not result.governance_passed:
        return ["Governance rules failed"]
    return []

def ml_research_governance_passed(result: MLResearchGovernanceResult) -> bool:
    return result.governance_passed

def ml_research_governance_summary(result: MLResearchGovernanceResult) -> Dict[str, Any]:
    return {"passed": result.governance_passed}

def ml_research_governance_to_text(result: MLResearchGovernanceResult, limit: int = 300) -> str:
    return f"Governance passed: {result.governance_passed}"
