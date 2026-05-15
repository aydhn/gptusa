import pytest
from usa_signal_bot.regime_map.walk_forward_adapter import attach_regime_map_to_walk_forward_result

def test_attach_regime_map_to_walk_forward_result():
    result = {"windows": []}
    enriched = attach_regime_map_to_walk_forward_result(result, None)
    assert "metadata" not in enriched  # it shouldn't be there if reviews_by_window is None
