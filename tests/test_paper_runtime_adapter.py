import sys
from unittest.mock import MagicMock
import pytest

# The target file imports FinalHandoffFullReview from final_handoff_models,
# but it doesn't exist in that file in this branch/setup. We must mock it
# safely without global mutation. We can patch it in sys.modules safely.
from unittest.mock import patch

class MockFinalHandoffModels:
    class FinalHandoffFullReview:
        pass

# Apply patch.dict to sys.modules specifically around the import of the target module
with patch.dict('sys.modules', {'usa_signal_bot.paper_final_handoff.final_handoff_models': MockFinalHandoffModels}):
    from usa_signal_bot.paper_final_handoff.paper_runtime_adapter import (
        build_read_only_paper_snapshot_for_final_handoff,
        compare_final_handoff_to_paper_snapshot,
        validate_paper_runtime_not_mutated_by_final_handoff,
        attach_final_handoff_metadata_to_paper_analytics,
        paper_runtime_final_handoff_adapter_to_text,
    )

def test_build_read_only_paper_snapshot_for_final_handoff_empty():
    res = build_read_only_paper_snapshot_for_final_handoff(None)
    assert res == {"paper_state_committed": False, "paper_order_executed": False, "portfolio_state_mutated": False}
    res2 = build_read_only_paper_snapshot_for_final_handoff({})
    assert res2 == {"paper_state_committed": False, "paper_order_executed": False, "portfolio_state_mutated": False}

def test_build_read_only_paper_snapshot_for_final_handoff_populated():
    payload = {"some_key": "some_value"}
    res = build_read_only_paper_snapshot_for_final_handoff(payload)
    assert res == payload
    assert res is not payload

def test_compare_final_handoff_to_paper_snapshot():
    # Pass a MagicMock instead of mutating module attributes globally
    review = MagicMock()
    res = compare_final_handoff_to_paper_snapshot(review, {})
    assert res == {"mutated": False}

def test_validate_paper_runtime_not_mutated_by_final_handoff():
    res = validate_paper_runtime_not_mutated_by_final_handoff({}, {})
    assert res == []

def test_attach_final_handoff_metadata_to_paper_analytics():
    payload = {"k": "v"}
    review = MagicMock()
    res = attach_final_handoff_metadata_to_paper_analytics(payload, review)
    assert res == payload
    assert res is payload

def test_paper_runtime_final_handoff_adapter_to_text():
    res = paper_runtime_final_handoff_adapter_to_text({})
    assert res == "PaperRuntimeAdapter Read-Only Snapshot"
