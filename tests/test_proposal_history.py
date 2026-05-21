from usa_signal_bot.paper_observation.proposal_history import (
    aggregate_proposal_history, count_proposals_by_type, count_proposals_by_status,
    proposal_history_warnings, proposal_history_to_text
)

def test_proposal_history():
    sessions = [
        {"proposals": [{"type": "BUY", "status": "BLOCKED"}, {"type": "SELL", "status": "APPROVED"}]}
    ]

    counts_t = count_proposals_by_type(sessions)
    assert counts_t["BUY"] == 1

    counts_s = count_proposals_by_status(sessions)
    assert counts_s["BLOCKED"] == 1

    warnings = proposal_history_warnings(sessions)
    assert len(warnings) == 1

    agg = aggregate_proposal_history(sessions)
    assert agg["total_proposals"] == 2

    text = proposal_history_to_text(agg)
    assert "Total: 2" in text
