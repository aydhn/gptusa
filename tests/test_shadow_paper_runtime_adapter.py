import pytest
from usa_signal_bot.paper_shadow.paper_runtime_adapter import (
    build_shadow_context_from_paper_runtime_snapshot,
    copy_paper_snapshot_to_shadow_portfolio,
    validate_no_paper_runtime_mutation,
    paper_runtime_shadow_adapter_to_text
)

def test_shadow_paper_runtime_adapter():
    snap = {"equity_usd": 150000.0, "positions": [{"symbol": "AAPL", "quantity": 10}]}
    ctx = build_shadow_context_from_paper_runtime_snapshot(snap)
    assert ctx.starting_equity_usd == 150000.0

    port = copy_paper_snapshot_to_shadow_portfolio(snap)
    assert port.equity_usd == 150000.0
    assert len(port.positions) == 1

    errs = validate_no_paper_runtime_mutation({}, {"paper_state_committed": True})
    assert len(errs) == 1

    text = paper_runtime_shadow_adapter_to_text({})
    assert "Paper Runtime Adapter Summary" in text
