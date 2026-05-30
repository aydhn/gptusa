import pytest
from usa_signal_bot.regime_classification.validation.data_quality_context_validator import detect_data_quality_limited_contexts

def test_detect_data_quality_limited_contexts():
    comp_res = [
        {"data_quality_limited": True},
        {"data_quality_limited": False}
    ]
    dq = detect_data_quality_limited_contexts(comp_res)
    assert len(dq) == 1
