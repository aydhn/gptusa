import pytest
from usa_signal_bot.feature_engine.integration_freeze.report_qa_acceptance import build_report_qa_acceptance_gate

def test_report_qa_acceptance_gate_safe():
    payload = {"text": "This is a local metadata report detailing correlation."}
    gate = build_report_qa_acceptance_gate(payload, [])
    assert gate.accepted == True
    assert gate.unsafe_language_count == 0

def test_report_qa_acceptance_gate_unsafe():
    payload = {"text": "Kesin al, this is a buy signal!"}
    gate = build_report_qa_acceptance_gate(payload, [])
    assert gate.accepted == False
    assert gate.unsafe_language_count > 0
    assert gate.trade_signal_language_detected == True
    assert gate.order_language_detected == True
