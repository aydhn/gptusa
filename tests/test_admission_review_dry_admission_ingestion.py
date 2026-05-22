from usa_signal_bot.paper_admission_review.dry_admission_ingestion import (
    ingest_dry_admission_full_review,
    dry_admission_supports_admission_review
)

def test_ingest_dry_admission_full_review():
    payload = {
        "activation_allowed": True,
        "all_writes_blocked": False,
        "mutation_detected": True,
    }
    result = ingest_dry_admission_full_review(payload)
    assert len(result.get("warnings", [])) >= 3
    assert "activation_allowed is true, blocking" in result["warnings"]
    assert "all_writes_blocked is false, blocking" in result["warnings"]
    assert "mutation_detected is true, blocking" in result["warnings"]

def test_dry_admission_supports_admission_review():
    supported, warnings = dry_admission_supports_admission_review({"decision": "RUN_DRY_ADMISSION_REHEARSAL"})
    assert supported
    assert len(warnings) == 0

    supported, warnings = dry_admission_supports_admission_review({"decision": "INVALID"})
    assert not supported
    assert len(warnings) == 1
