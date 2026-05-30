import pytest
from usa_signal_bot.regime_classification.validation.low_compatibility_reason_mapper import map_low_compatibility_reasons

def test_map_low_compatibility_reasons():
    comp_res = [
        {"compatibility_id": "1", "score": 20, "data_quality_limited": True},
        {"compatibility_id": "2", "score": 30}
    ]
    mapper = map_low_compatibility_reasons(comp_res, [])
    assert len(mapper) == 2
    assert "data_quality_limited" in mapper["1"]
    assert "compatibility_score_below_40" in mapper["2"]
