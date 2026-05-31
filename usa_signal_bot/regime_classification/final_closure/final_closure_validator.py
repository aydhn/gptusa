from typing import Any, Dict, List
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeResearchFreezeIngestionResult,
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    RegimeFinalClosureQuality,
    create_regime_final_closure_result_id
)
from usa_signal_bot.regime_classification.final_closure.final_closure_rules import build_final_closure_rules
from datetime import datetime, timezone

def run_final_closure_validation(ingestion: RegimeResearchFreezeIngestionResult, chain_validation: RegimeArtifactChainValidationResult) -> RegimeFinalClosureResult:
    rules = build_final_closure_rules(ingestion, chain_validation)

    passed = all(r.passed for r in rules)

    res = RegimeFinalClosureResult(
        closure_result_id=create_regime_final_closure_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rules=rules,
        artifact_chain_validation=chain_validation,
        total_rules=len(rules),
        passed_rules=sum(1 for r in rules if r.passed),
        failed_rules=sum(1 for r in rules if not r.passed),
        closure_passed=passed,
        ready_for_freeze_seal=passed,
        ready_for_phase136_kickoff_gate=passed,
        quality=RegimeFinalClosureQuality.HIGH if passed else RegimeFinalClosureQuality.LOW
    )
    return res

def final_closure_passed(result: RegimeFinalClosureResult) -> bool:
    return result.closure_passed

def final_closure_blocks_phase136(result: RegimeFinalClosureResult) -> bool:
    return not result.ready_for_phase136_kickoff_gate

def validate_final_closure_result(result: RegimeFinalClosureResult) -> List[str]:
    return []

def final_closure_validation_summary(result: RegimeFinalClosureResult) -> Dict[str, Any]:
    return {"closure_passed": result.closure_passed}

def final_closure_validation_to_text(result: RegimeFinalClosureResult, limit: int = 300) -> str:
    return f"Closure Passed: {result.closure_passed}"
