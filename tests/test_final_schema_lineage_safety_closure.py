import pytest
from usa_signal_bot.feature_engine.final_closure.freeze_preparation_ingestion import ingest_freeze_preparation_review_payload
from usa_signal_bot.feature_engine.final_closure.final_artifact_chain_loader import build_final_artifact_references
from usa_signal_bot.feature_engine.final_closure.final_schema_lineage_safety_closure import build_schema_lineage_safety_closure_rule

def test_build_schema_lineage_safety_closure_rule_pass():
    payload = {"context": {"ready_for_phase125": True}}
    ingestion = ingest_freeze_preparation_review_payload(payload)
    artifacts = build_final_artifact_references()
    rule = build_schema_lineage_safety_closure_rule(ingestion, artifacts)
    assert rule.passed is True

def test_build_schema_lineage_safety_closure_rule_fail():
    payload = {"context": {"produces_trade_signal": True}}
    ingestion = ingest_freeze_preparation_review_payload(payload)
    artifacts = build_final_artifact_references()
    rule = build_schema_lineage_safety_closure_rule(ingestion, artifacts)
    assert rule.passed is False
