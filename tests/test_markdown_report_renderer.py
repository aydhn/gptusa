import pytest
from usa_signal_bot.feature_engine.factor_explainability.markdown_report_renderer import validate_rendered_markdown

def test_validate_rendered_markdown():
    res = validate_rendered_markdown("This has a buy signal here")
    assert len(res) > 0
    assert "signal" in res[0].lower()
