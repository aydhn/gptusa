
from usa_signal_bot.core_runtime_acceptance.foundation_freeze import (
    build_advanced_foundation_freeze_bundle
)
from usa_signal_bot.core_runtime_acceptance.phase105_models import ConsolidationEvidenceItem

def test_foundation_freeze_bundle():
    evidence = [ConsolidationEvidenceItem(
        evidence_id="ev1",
        created_at_utc="now",
        evidence_type="type1",
        source_phase=101,
        available=True,
        fresh=True,
        stale=False
    )]
    bundle = build_advanced_foundation_freeze_bundle(evidence)
    assert bundle.frozen == True
    assert bundle.immutable == True
    assert bundle.missing_evidence_count == 0
