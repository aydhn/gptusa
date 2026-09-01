import pytest
from unittest.mock import MagicMock, patch

from usa_signal_bot.paper_final_handoff.final_handoff_reporting import (
    final_handoff_evidence_ref_to_text,
    final_handoff_review_to_text,
    sealed_archive_manifest_to_text,
    archive_integrity_report_to_text,
    pre_paper_checkpoint_gate_to_text,
    pre_paper_governance_checkpoint_to_text,
    final_handoff_audit_entry_to_text,
    final_handoff_full_review_to_text,
    final_handoff_store_summary_to_text
)

def test_final_handoff_evidence_ref_to_text():
    item = MagicMock()
    item.evidence_ref_id = 'ev_123'
    assert final_handoff_evidence_ref_to_text(item) == 'EvidenceRef: ev_123'

def test_final_handoff_review_to_text():
    item = MagicMock()
    item.handoff_review_id = 'rev_123'
    item.status.value = 'APPROVED'
    assert final_handoff_review_to_text(item) == 'Review: rev_123 [APPROVED]'

def test_sealed_archive_manifest_to_text():
    item = MagicMock()
    item.archive_id = 'arch_123'
    item.status.value = 'SEALED'
    assert sealed_archive_manifest_to_text(item) == 'Manifest: arch_123 [SEALED]'

def test_archive_integrity_report_to_text():
    item = MagicMock()
    item.status.value = 'VALID'
    assert archive_integrity_report_to_text(item) == 'Integrity: VALID'

def test_pre_paper_checkpoint_gate_to_text():
    item = MagicMock()
    item.gate_name = 'gate_1'
    item.status.value = 'PASSED'
    assert pre_paper_checkpoint_gate_to_text(item) == 'Gate: gate_1 [PASSED]'

def test_pre_paper_governance_checkpoint_to_text():
    item = MagicMock()
    item.checkpoint_id = 'chk_123'
    item.status.value = 'VERIFIED'
    assert pre_paper_governance_checkpoint_to_text(item) == 'Checkpoint: chk_123 [VERIFIED]'

def test_final_handoff_audit_entry_to_text():
    item = MagicMock()
    item.audit_id = 'aud_123'
    item.action = 'CREATE'
    assert final_handoff_audit_entry_to_text(item) == 'Audit: aud_123 [CREATE]'

@patch('usa_signal_bot.paper_final_handoff.final_handoff_reporting.final_handoff_limitations_text')
def test_final_handoff_full_review_to_text(mock_limitations):
    mock_limitations.return_value = 'LIMITATIONS: ...'
    item = MagicMock()
    item.review_id = 'full_rev_1'
    item.handoff_reviews = [MagicMock(), MagicMock()]
    item.archive_manifests = [MagicMock()]
    res = final_handoff_full_review_to_text(item)
    assert 'FinalHandoffFullReview: full_rev_1' in res
    assert 'Reviews: 2' in res
    assert 'Manifests: 1' in res
    assert 'LIMITATIONS: ...' in res

def test_final_handoff_store_summary_to_text():
    summary = {'key': 'value'}
    assert final_handoff_store_summary_to_text(summary) == "Store Summary: {'key': 'value'}"
