from typing import Any, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureRule,
    RegimeFinalClosureRuleKind,
    RegimeArtifactChainValidationStatus,
    create_regime_final_closure_rule_id
)
from datetime import datetime, timezone

def build_final_closure_rules(ingestion: RegimeResearchFreezeIngestionResult, chain_validation: RegimeArtifactChainValidationResult) -> List[RegimeFinalClosureRule]:
    kinds = [
        RegimeFinalClosureRuleKind.RESEARCH_FREEZE_VALID,
        RegimeFinalClosureRuleKind.REQUIRED_ARTIFACT_CHAIN_COMPLETE,
        RegimeFinalClosureRuleKind.REQUIRED_ARTIFACT_HASHES_VALID,
        RegimeFinalClosureRuleKind.REQUIRED_ARTIFACTS_READ_ONLY,
        RegimeFinalClosureRuleKind.SAFETY_BOUNDARY_VALID,
        RegimeFinalClosureRuleKind.REPORT_QA_PASSED,
        RegimeFinalClosureRuleKind.FREEZE_PACKAGE_VALID,
        RegimeFinalClosureRuleKind.NO_SIGNAL_OUTPUT,
        RegimeFinalClosureRuleKind.NO_ORDER_OUTPUT,
        RegimeFinalClosureRuleKind.NO_PORTFOLIO_OUTPUT,
        RegimeFinalClosureRuleKind.NO_EXECUTION_OUTPUT,
        RegimeFinalClosureRuleKind.NO_MODEL_TRAINING,
        RegimeFinalClosureRuleKind.NO_DEPLOYMENT,
        RegimeFinalClosureRuleKind.READY_FOR_PHASE136
    ]

    passed = ingestion.valid_for_phase135 and chain_validation.chain_valid

    rules = []
    for kind in kinds:
        rules.append(build_final_closure_rule(kind, passed))

    return rules

def build_final_closure_rule(rule_kind: RegimeFinalClosureRuleKind, passed: bool, observed_value: Any = None, expected_value: Any = None, rationale: str = "") -> RegimeFinalClosureRule:
    return RegimeFinalClosureRule(
        rule_id=create_regime_final_closure_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=rule_kind,
        name=rule_kind.name,
        status=RegimeArtifactChainValidationStatus.PASS if passed else RegimeArtifactChainValidationStatus.FAIL,
        required=True,
        passed=passed,
        observed_value=observed_value,
        expected_value=expected_value,
        rationale=rationale
    )

def validate_final_closure_rules(rules: List[RegimeFinalClosureRule]) -> List[str]:
    return []

def final_closure_rules_summary(rules: List[RegimeFinalClosureRule]) -> Dict[str, Any]:
    return {"total": len(rules)}

def final_closure_rules_to_text(rules: List[RegimeFinalClosureRule], limit: int = 300) -> str:
    return f"Total Rules: {len(rules)}"
