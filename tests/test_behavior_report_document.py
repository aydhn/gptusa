from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import (
    RegimeTransitionIngestionResult
)
from usa_signal_bot.regime_classification.behavior_reporting.behavior_report_document import (
    build_behavior_report_document, validate_behavior_report_document
)

def test_build_behavior_report_document():
    ing = RegimeTransitionIngestionResult()
    doc = build_behavior_report_document(ing, [], [], [])
    assert doc.title == "Market Behavior Report"
    assert len(doc.sections) == 11
    assert doc.document_hash is not None

def test_validate_behavior_report_document():
    ing = RegimeTransitionIngestionResult()
    doc = build_behavior_report_document(ing, [], [], [])
    errs = validate_behavior_report_document(doc)
    assert not errs
