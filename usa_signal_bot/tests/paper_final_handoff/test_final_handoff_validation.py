import sys
from unittest.mock import MagicMock

class CatchAllMockException(Exception): pass

class MockExceptions:
    def __getattr__(self, name):
        return CatchAllMockException

sys.modules['usa_signal_bot.core.exceptions'] = MockExceptions()

class MockFinalHandoffModels:
    class FinalHandoffReview:
        pass
    class SealedReadinessArchiveManifest:
        pass
    class PrePaperGovernanceCheckpoint:
        pass
    class FinalHandoffFullReview:
        pass
sys.modules['usa_signal_bot.paper_final_handoff.final_handoff_models'] = MockFinalHandoffModels

import pytest
from usa_signal_bot.paper_final_handoff.final_handoff_validation import (
    validate_final_handoff_review_report,
    validate_archive_manifest_report,
    validate_pre_paper_checkpoint_report,
    validate_final_handoff_full_review_report,
    validate_no_sensitive_data_in_final_handoff_payload,
    validate_no_live_execution_language_in_final_handoff,
    validate_no_active_paper_language_in_final_handoff,
    validate_no_paper_state_mutation_fields_in_final_handoff,
    validate_no_broker_execution_fields_in_final_handoff,
    final_handoff_validation_report_to_text,
    assert_final_handoff_valid,
    FinalHandoffValidationReport,
    FinalHandoffValidationIssue,
)
from usa_signal_bot.core.exceptions import FinalHandoffValidationError

# Mock the imports for the data types used in functions
class MockFinalHandoffReview:
    def __init__(self, allows_active_paper=False, allows_broker_execution=False):
        self.allows_active_paper = allows_active_paper
        self.allows_broker_execution = allows_broker_execution

class MockSealedReadinessArchiveManifest:
    def __init__(self, sealed=False, immutable=False):
        self.sealed = sealed
        self.immutable = immutable

def test_validate_final_handoff_review_report_valid():
    item = MockFinalHandoffReview(allows_active_paper=False, allows_broker_execution=False)
    report = validate_final_handoff_review_report(item)
    assert report.valid is True
    assert report.error_count == 0
    assert len(report.issues) == 0

def test_validate_final_handoff_review_report_invalid_active_paper():
    item = MockFinalHandoffReview(allows_active_paper=True, allows_broker_execution=False)
    report = validate_final_handoff_review_report(item)
    assert report.valid is False
    assert report.error_count == 1
    assert report.issues[0].field == "allows_active_paper"

def test_validate_final_handoff_review_report_invalid_broker_execution():
    item = MockFinalHandoffReview(allows_active_paper=False, allows_broker_execution=True)
    report = validate_final_handoff_review_report(item)
    assert report.valid is False
    assert report.error_count == 1
    assert report.issues[0].field == "allows_broker_execution"

def test_validate_final_handoff_review_report_invalid_both():
    item = MockFinalHandoffReview(allows_active_paper=True, allows_broker_execution=True)
    report = validate_final_handoff_review_report(item)
    assert report.valid is False
    assert report.error_count == 2

def test_validate_archive_manifest_report_valid_unsealed():
    item = MockSealedReadinessArchiveManifest(sealed=False, immutable=False)
    report = validate_archive_manifest_report(item)
    assert report.valid is True
    assert report.error_count == 0

def test_validate_archive_manifest_report_valid_sealed_immutable():
    item = MockSealedReadinessArchiveManifest(sealed=True, immutable=True)
    report = validate_archive_manifest_report(item)
    assert report.valid is True
    assert report.error_count == 0

def test_validate_archive_manifest_report_invalid_sealed_mutable():
    item = MockSealedReadinessArchiveManifest(sealed=True, immutable=False)
    report = validate_archive_manifest_report(item)
    assert report.valid is False
    assert report.error_count == 1
    assert report.issues[0].field == "immutable"

def test_validate_pre_paper_checkpoint_report():
    report = validate_pre_paper_checkpoint_report(MagicMock())
    assert report.valid is True
    assert report.error_count == 0

def test_validate_final_handoff_full_review_report():
    report = validate_final_handoff_full_review_report(MagicMock())
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_sensitive_data_in_final_handoff_payload_valid():
    payload = {"public_key": "abc", "data": "123"}
    report = validate_no_sensitive_data_in_final_handoff_payload(payload)
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_sensitive_data_in_final_handoff_payload_invalid_api_key():
    payload = {"API_key": "12345"}
    report = validate_no_sensitive_data_in_final_handoff_payload(payload)
    assert report.valid is False
    assert report.error_count == 1

def test_validate_no_sensitive_data_in_final_handoff_payload_invalid_secret():
    payload = {"my_SECRET": "xyz"}
    report = validate_no_sensitive_data_in_final_handoff_payload(payload)
    assert report.valid is False
    assert report.error_count == 1

def test_validate_no_live_execution_language_in_final_handoff_valid():
    report = validate_no_live_execution_language_in_final_handoff("This is a safe test message.")
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_live_execution_language_in_final_handoff_invalid():
    report = validate_no_live_execution_language_in_final_handoff("This order is SENT to Broker now.")
    assert report.valid is False
    assert report.error_count == 1

def test_validate_no_active_paper_language_in_final_handoff_valid():
    report = validate_no_active_paper_language_in_final_handoff("Just running some passive tests.")
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_active_paper_language_in_final_handoff_invalid():
    report = validate_no_active_paper_language_in_final_handoff("Please Canlıya al this change.")
    assert report.valid is False
    assert report.error_count == 1

def test_validate_no_paper_state_mutation_fields_in_final_handoff_valid():
    payload = {"id": 1, "status": "ok"}
    report = validate_no_paper_state_mutation_fields_in_final_handoff(payload)
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_paper_state_mutation_fields_in_final_handoff_invalid():
    payload = {"paper_state_committed": True}
    report = validate_no_paper_state_mutation_fields_in_final_handoff(payload)
    assert report.valid is False
    assert report.error_count == 1

def test_validate_no_broker_execution_fields_in_final_handoff_valid():
    payload = {"internal_id": 123}
    report = validate_no_broker_execution_fields_in_final_handoff(payload)
    assert report.valid is True
    assert report.error_count == 0

def test_validate_no_broker_execution_fields_in_final_handoff_invalid():
    payload = {"live_order_id": "ABC"}
    report = validate_no_broker_execution_fields_in_final_handoff(payload)
    assert report.valid is False
    assert report.error_count == 1
    assert report.issues[0].message == "Found broker field: live_order_id"

def test_final_handoff_validation_report_to_text():
    report = FinalHandoffValidationReport(valid=False, issue_count=2, warning_count=0, error_count=2, blocked_count=0, issues=[], warnings=[], errors=[])
    text = final_handoff_validation_report_to_text(report)
    assert text == "Valid: False, Errors: 2"

def test_assert_final_handoff_valid():
    report = FinalHandoffValidationReport(valid=True, issue_count=0, warning_count=0, error_count=0, blocked_count=0, issues=[], warnings=[], errors=[])
    # Should not raise
    assert_final_handoff_valid(report)

def test_assert_final_handoff_invalid():
    report = FinalHandoffValidationReport(valid=False, issue_count=1, warning_count=0, error_count=1, blocked_count=0, issues=[], warnings=[], errors=[])
    with pytest.raises(FinalHandoffValidationError, match="Final handoff validation failed."):
        assert_final_handoff_valid(report)
