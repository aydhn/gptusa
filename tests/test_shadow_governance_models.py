import pytest
from usa_signal_bot.core.enums import ShadowAcceptanceStatus, ShadowGovernanceDecision
from usa_signal_bot.core.exceptions import ShadowGovernanceValidationError
from usa_signal_bot.paper_shadow_governance.shadow_governance_models import (
    ShadowAcceptanceScorecard, ShadowDecisionBoardResult,
    create_shadow_acceptance_scorecard_id, utc_now_iso
)

def test_scorecard_validation():
    sc = ShadowAcceptanceScorecard(
        scorecard_id="test", created_at_utc=utc_now_iso(),
        baseline_session_id=None, candidate_session_id=None,
        overall_status=ShadowAcceptanceStatus.PASS, acceptance_score=100.0,
        gate_pass_count=0, gate_warning_count=0, gate_fail_count=0, gate_blocked_count=0,
        metric_score_components={}, risk_flags=[], manual_review_required=True,
        allowed_for_real_orders=True, allowed_for_paper_state_mutation=False,
        allowed_for_telegram_real_send=False, allowed_for_production_config_write=False,
        warnings=[], errors=[]
    )
    from usa_signal_bot.paper_shadow_governance.shadow_governance_models import validate_shadow_acceptance_scorecard
    with pytest.raises(ShadowGovernanceValidationError, match="real orders"):
        validate_shadow_acceptance_scorecard(sc)
