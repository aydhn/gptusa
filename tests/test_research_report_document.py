import pytest
from usa_signal_bot.feature_engine.factor_explainability.research_report_document import compute_research_report_hash, build_research_report_document
from usa_signal_bot.feature_engine.factor_explainability.phase123_models import FactorExplanationReport, ExplainabilityInputBundle, FactorExplainabilityQuality

def test_build_research_report_document():
    # Setup dummy inputs
    exp = FactorExplanationReport("id", "", "", [], [], [], [], FactorExplainabilityQuality.ACCEPTABLE, True, True, False, False, False, False, [], [], [], {})
    bundle = ExplainabilityInputBundle("b_id", "", "", {}, [], [], [], "", "", "", True, True, True, [], [], [], {})
    doc = build_research_report_document(exp, bundle)
    assert len(doc.sections) > 0
    assert doc.document_hash is not None
