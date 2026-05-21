from usa_signal_bot.paper_controlled_planning.adjacent_proposal_builder import (
    build_adjacent_proposals, validate_adjacent_proposals_safe
)
from usa_signal_bot.paper_controlled_planning.adjacent_rehearsal_context import build_mock_paper_adjacent_rehearsal_context

def test_adjacent_proposal():
    ctx = build_mock_paper_adjacent_rehearsal_context()
    props = build_adjacent_proposals(ctx)
    assert len(props) == 2
    assert not validate_adjacent_proposals_safe(props)

    props[0].is_real_order = True
    assert len(validate_adjacent_proposals_safe(props)) == 1
