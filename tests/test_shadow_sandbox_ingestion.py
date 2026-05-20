from usa_signal_bot.paper_shadow.sandbox_ingestion import (
    ingest_sandbox_review_payload, extract_sandbox_context_payload,
    extract_sandbox_bundle_refs, extract_sandbox_preview_outputs,
    sandbox_ingestion_warnings, sandbox_ingestion_to_text
)

def test_ingest_sandbox_review_payload():
    payload = {"context": {"id": "c1"}, "bundle_refs": {"id": "b1"}, "preview_outputs": []}
    res = ingest_sandbox_review_payload(payload)
    assert res["status"] == "ingested"
    assert res["context"]["id"] == "c1"
    assert res["bundle_refs"]["id"] == "b1"

def test_extract_sandbox_context_payload():
    assert extract_sandbox_context_payload({"context": {"id": "c1"}}) == {"id": "c1"}

def test_extract_sandbox_bundle_refs():
    assert extract_sandbox_bundle_refs({"bundle_refs": {"id": "b1"}}) == {"id": "b1"}

def test_extract_sandbox_preview_outputs():
    assert extract_sandbox_preview_outputs({"preview_outputs": [{"a": 1}]}) == [{"a": 1}]

def test_sandbox_ingestion_warnings():
    assert len(sandbox_ingestion_warnings({})) == 1
    assert len(sandbox_ingestion_warnings({"context": {}})) == 0
    assert len(sandbox_ingestion_warnings({"context": {}, "unsafe_flags": ["real_order"]})) == 1

def test_sandbox_ingestion_to_text():
    assert "Warnings: 1" in sandbox_ingestion_to_text({})
