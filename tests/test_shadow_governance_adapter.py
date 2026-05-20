from usa_signal_bot.paper_shadow.governance_adapter import (
    governance_shadow_allowed, shadow_rehearsal_governance_checklist,
    attach_shadow_rehearsal_to_governance_payload
)
from usa_signal_bot.paper_shadow.shadow_models import ShadowRehearsalSession

def test_governance_shadow_allowed():
    allowed, errs = governance_shadow_allowed({})
    assert allowed
    assert len(errs) == 0

def test_attach_shadow_rehearsal_to_governance_payload():
    session = ShadowRehearsalSession(
        session_id="s1", created_at_utc="", status="COMPLETED",
        context=None, portfolio_state=None, signals=[], order_intents=[], fills=[],
        ledger_events=[], pnl_snapshots=[], safety_flags=[], started_at_utc=None,
        completed_at_utc=None, output_paths={}, warnings=[], errors=[]
    )
    payload = attach_shadow_rehearsal_to_governance_payload({}, session)
    assert "shadow_rehearsal_metadata" in payload
    assert payload["shadow_rehearsal_metadata"]["status"] == "COMPLETED"
