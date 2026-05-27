import pytest
from usa_signal_bot.feature_engine.factor_explainability.lineage_quality_interpretation import interpret_lineage_quality_context

def test_interpret_lineage_quality_context():
    res = interpret_lineage_quality_context()
    assert "approved" in res[0].lower()
