import pytest
from usa_signal_bot.regime_map.dispersion_proxy import dispersion_score, dispersion_proxy_summary_to_text

def test_dispersion_score_insufficient():
    assert dispersion_score([]) is None

def test_dispersion_proxy_summary_to_text():
    text = dispersion_proxy_summary_to_text({"dispersion_score": 55.5})
    assert "55.5" in text
