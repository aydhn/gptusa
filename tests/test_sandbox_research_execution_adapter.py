import pytest
from usa_signal_bot.release_sandbox.research_execution_adapter import (
    sandbox_preview_from_research_execution_payload,
    attach_sandbox_preview_to_execution_payload,
    research_execution_adapter_to_text,
    research_execution_sandbox_summary
)

def test_research_execution_adapter():
    payload = {"execution_id": "e1"}

    out = sandbox_preview_from_research_execution_payload(payload)
    assert out.output_type == "RESEARCH_EXECUTION_PREVIEW"
    assert out.summary["execution_id"] == "e1"

    payload = attach_sandbox_preview_to_execution_payload(payload, out)
    assert "sandbox_preview_id" in payload

    txt = research_execution_adapter_to_text(payload)
    assert "Has Sandbox Preview = True" in txt


def test_research_execution_sandbox_summary():
    payload_without = {"execution_id": "e1"}
    summary_without = research_execution_sandbox_summary(payload_without)
    assert summary_without["has_sandbox_preview"] is False

    payload_with = {"execution_id": "e1", "sandbox_preview_id": "some_id"}
    summary_with = research_execution_sandbox_summary(payload_with)
    assert summary_with["has_sandbox_preview"] is True
