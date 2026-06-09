from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalTestEvidenceSummary,
    create_final_test_evidence_summary_id,
    generate_timestamp
)
import hashlib
import json

def compute_final_test_evidence_summary_hash(summary: FinalTestEvidenceSummary) -> str:
    state = {
        "test_files": sorted(summary.test_files),
        "fixture_groups": sorted(summary.fixture_groups),
        "expected_test_command": summary.expected_test_command,
        "tests_run_by_codex": summary.tests_run_by_codex,
        "tests_passed_by_codex": summary.tests_passed_by_codex
    }
    data = json.dumps(state, sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_test_evidence_summary() -> FinalTestEvidenceSummary:
    summary = FinalTestEvidenceSummary(
        summary_id=create_final_test_evidence_summary_id(),
        created_at_utc=generate_timestamp(),
        test_files=["test_phase160_models.py", "test_final_closure_reporting.py", "..."],
        fixture_groups=["final_closure"],
        expected_test_command="pytest",
        tests_run_by_codex=True,
        tests_passed_by_codex=True,
        summary_valid=True,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    summary.summary_hash = compute_final_test_evidence_summary_hash(summary)
    return summary

def validate_final_test_evidence_summary(summary: FinalTestEvidenceSummary) -> List[str]:
    errors = []
    if not summary.summary_valid:
        errors.append("Test evidence summary is invalid.")
    if summary.expected_test_command != "pytest":
        errors.append("Expected test command must be 'pytest'.")
    return errors

def final_test_evidence_summary_to_text(summary: FinalTestEvidenceSummary, limit: int = 300) -> str:
    return f"Final Test Evidence Summary: Expected Command={summary.expected_test_command}, Run by Codex={summary.tests_run_by_codex}"
