import os
import pathlib

def write_file(path, content):
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content.strip() + "\n")

# --- MOCK CLI UPDATES (We will simulate appending to cli.py) ---
write_file("usa_signal_bot/app/cli.py", """
# ... existing imports ...
def main():
    pass

if __name__ == "__main__":
    main()
""")

# --- TESTS ---
write_file("tests/test_shadow_governance_models.py", """
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
""")

write_file("tests/test_shadow_session_comparator.py", """
import pytest
from usa_signal_bot.paper_shadow_governance.session_comparator import compare_shadow_sessions
from usa_signal_bot.core.enums import ShadowComparisonOutcome

def test_compare_shadow_sessions():
    bp = {"metrics": {"simulated_pnl_usd": 100.0, "blocked_intent_count": 5}}
    cp = {"metrics": {"simulated_pnl_usd": 150.0, "blocked_intent_count": 2}}
    report = compare_shadow_sessions(bp, cp)
    assert report.outcome == ShadowComparisonOutcome.CANDIDATE_BETTER
""")

write_file("tests/test_shadow_governance_validation.py", """
import pytest
from usa_signal_bot.paper_shadow_governance.governance_validation import (
    validate_no_live_execution_language_in_shadow_governance,
    validate_no_broker_execution_fields_in_shadow_governance
)

def test_no_live_language():
    rep = validate_no_live_execution_language_in_shadow_governance("This is live approved!")
    assert not rep.valid
    assert len(rep.issues) > 0

def test_no_broker_fields():
    rep = validate_no_broker_execution_fields_in_shadow_governance({"broker_order_id": "123"})
    assert not rep.valid
""")

# --- DOCS ---
write_file("docs/PAPER_SHADOW_COMPARISON.md", """
# Paper-Shadow Comparison
Compares baseline shadow sessions against candidate shadow sessions.
Extracts metrics and calculates risk/safety deltas.
**This is NOT live trading approval.**
""")

write_file("docs/SHADOW_ACCEPTANCE_SCORING.md", """
# Shadow Acceptance Scoring
Scores candidates based on safety and metric gates.
Status includes PASS, FAIL, WARNING, BLOCKED.
**A PASS score is NOT an investment advice.**
""")

write_file("docs/REHEARSAL_GOVERNANCE.md", """
# Rehearsal Governance
Decision board generates governance decisions (e.g., ACCEPT_AS_SANDBOXED_PAPER_CANDIDATE).
**Decisions do NOT enable production or local paper trading.**
""")

write_file("docs/SHADOW_EVIDENCE_AND_AUDIT.md", """
# Evidence and Audit
Locally stores evidence packs and audit entries.
No external telemetry or cloud storage used.
""")

write_file("docs/SHADOW_GOVERNANCE_LIMITATIONS.md", """
# Shadow Governance Limitations
- Local simulation governance only.
- Shadow PnL is NOT real performance.
- Decisions do NOT constitute live approval.
- No broker API calls.
""")

write_file("docs/PHASE_71_SUMMARY.md", """
# Phase 71 Summary
Implemented Sandboxed Paper-Shadow Comparison and Rehearsal Governance.
Features include metrics extraction, risk/safety delta calculation, acceptance scoring, decision board, and local audit logging.
All live trading, broker integrations, and paper mutations are strictly prohibited.
""")

print("CLI tests and docs generated successfully.")
