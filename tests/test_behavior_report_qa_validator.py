from usa_signal_bot.regime_classification.behavior_reporting.phase130_models import BehaviorReportDocument
from usa_signal_bot.regime_classification.behavior_reporting.behavior_report_qa_validator import (
    run_behavior_report_qa, behavior_report_qa_passed
)

def test_run_behavior_report_qa_pass():
    doc = BehaviorReportDocument(title="Safe Report")
    results = run_behavior_report_qa(doc, "This is a strictly research metadata report.")
    assert behavior_report_qa_passed(results)

def test_run_behavior_report_qa_fail():
    doc = BehaviorReportDocument(title="Unsafe Report")
    results = run_behavior_report_qa(doc, "This is a strong buy signal. Sent to broker.")
    assert not behavior_report_qa_passed(results)

    fails = [r for r in results if not r.passed]
    assert len(fails) > 0
