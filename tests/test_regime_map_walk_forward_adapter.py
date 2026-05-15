from usa_signal_bot.regime_map.walk_forward_adapter import attach_regime_map_to_walk_forward_result

def test_attach_wf():
    res = {"metrics": {}}
    out = attach_regime_map_to_walk_forward_result(res, None)
    assert out["metadata"]["regime_map_attached"] == True
