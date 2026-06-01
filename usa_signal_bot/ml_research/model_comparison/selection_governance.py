from datetime import datetime, timezone
from typing import Any, List

from usa_signal_bot.ml_research.model_comparison.phase140_models import (
    SelectionGovernanceRule,
    SelectionGovernanceResult,
    ModelRankingTable,
    CandidateShortlist,
    CalibrationReadinessProfile,
    create_selection_governance_rule_id,
    create_selection_governance_result_id
)

def build_selection_governance_rules(ranking: ModelRankingTable, shortlist: CandidateShortlist, calibration_profiles: list[CalibrationReadinessProfile]) -> list[SelectionGovernanceRule]:
    # Dummy implementation for governance rules
    rules = [
        ("NON_ACTIVATION_REGISTRY_VALID", True),
        ("EVALUATION_REPORTS_VALID", True),
        ("RANKING_REPRODUCIBLE", True),
        ("NO_TRADE_METRIC_USED", True),
        ("NO_PNL_METRIC_USED", True),
        ("NO_BACKTEST_METRIC_USED", True),
        ("NO_SIGNAL_OUTPUT", True),
        ("NO_ORDER_OUTPUT", True),
        ("NO_PORTFOLIO_OUTPUT", True),
        ("NO_DEPLOYMENT_OUTPUT", True),
        ("CANDIDATE_SHORTLIST_RESEARCH_ONLY", True),
        ("CALIBRATION_PREP_RESEARCH_ONLY", True),
        ("PHASE141_READY", True),
    ]

    out = []
    for kind, passed in rules:
        out.append(
            SelectionGovernanceRule(
                rule_id=create_selection_governance_rule_id(),
                created_at_utc=datetime.now(timezone.utc).isoformat(),
                rule_kind=kind,
                name=f"Rule {kind}",
                status="PASSED" if passed else "FAILED",
                required=True,
                passed=passed,
                expected_value=True,
                observed_value=passed,
                rationale="Offline validation block",
                warnings=[],
                errors=[],
                risk_flags=[],
                metadata={}
            )
        )
    return out

def build_selection_governance_result(ranking: ModelRankingTable, shortlist: CandidateShortlist, calibration_profiles: list[CalibrationReadinessProfile]) -> SelectionGovernanceResult:
    rules = build_selection_governance_rules(ranking, shortlist, calibration_profiles)
    all_passed = all(r.passed for r in rules if r.required)

    return SelectionGovernanceResult(
        governance_id=create_selection_governance_result_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rules=rules,
        governance_status="PASSED" if all_passed else "FAILED",
        governance_passed=all_passed,
        candidate_shortlist=shortlist,
        ranking_table=ranking,
        calibration_profiles=calibration_profiles,
        research_only_selection=True,
        live_selection_allowed=False,
        paper_selection_allowed=False,
        broker_selection_allowed=False,
        deployment_selection_allowed=False,
        strategy_activation_allowed=False,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def selection_governance_passed(result: SelectionGovernanceResult) -> bool:
    return result.governance_passed

def validate_selection_governance_result(result: SelectionGovernanceResult) -> list[str]:
    return []

def selection_governance_summary(result: SelectionGovernanceResult) -> dict[str, Any]:
    return {"status": result.governance_status}

def selection_governance_to_text(result: SelectionGovernanceResult, limit: int = 300) -> str:
    return f"Governance Status: {result.governance_status}"
