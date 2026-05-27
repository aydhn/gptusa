import pytest
from usa_signal_bot.feature_engine.factor_explainability.json_report_renderer import validate_rendered_json

def test_validate_rendered_json():
    res = validate_rendered_json({})
    assert len(res) == 0
