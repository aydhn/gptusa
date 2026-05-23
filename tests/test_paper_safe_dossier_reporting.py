from usa_signal_bot.paper_safe_dossier.dossier_reporting import (
    paper_safe_dossier_evidence_item_to_text,
    runtime_component_map_item_to_text,
    paper_safe_dossier_audit_entry_to_text,
    paper_safe_dossier_store_summary_to_text
)
from usa_signal_bot.paper_safe_dossier.dossier_audit import create_paper_safe_dossier_audit_entry
from usa_signal_bot.paper_safe_dossier.dossier_evidence import evidence_item_from_paper_safe_source

def test_paper_safe_dossier_reporting():
    item = evidence_item_from_paper_safe_source("test", None)
    txt = paper_safe_dossier_evidence_item_to_text(item)
    assert "MISSING" in txt

    audit = create_paper_safe_dossier_audit_entry("Entity", "123", "ACTION", "Rationale")
    txt = paper_safe_dossier_audit_entry_to_text(audit)
    assert "ACTION" in txt

    summary = {"test": 123}
    txt = paper_safe_dossier_store_summary_to_text(summary)
    assert "123" in txt
