from usa_signal_bot.regime_classification.freeze_preparation.drift_report_qa_validator import run_drift_report_qa
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import DriftReportDocument

def test_run_drift_report_qa_safe():
    doc = DriftReportDocument(document_id="d1", created_at_utc="", title="Doc", sections=[], source_review_id="r1", rendered_markdown="", rendered_text="This is safe.", rendered_json=None, document_hash="", research_metadata_only=True, investment_advice=False, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, qa_status="NOT_CHECKED")
    res = run_drift_report_qa(doc)
    assert all(r.passed for r in res)

def test_run_drift_report_qa_unsafe():
    doc = DriftReportDocument(document_id="d1", created_at_utc="", title="Doc", sections=[], source_review_id="r1", rendered_markdown="", rendered_text="This is garanti kâr.", rendered_json=None, document_hash="", research_metadata_only=True, investment_advice=False, produces_trade_signal=False, produces_order_decision=False, produces_portfolio_weights=False, qa_status="NOT_CHECKED")
    res = run_drift_report_qa(doc)
    assert not all(r.passed for r in res)
