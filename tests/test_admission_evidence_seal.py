from usa_signal_bot.paper_admission_review.admission_evidence_seal import build_admission_evidence_seal
from usa_signal_bot.core.enums import AdmissionEvidenceSealStatus

def test_build_admission_evidence_seal():
    seal = build_admission_evidence_seal(evidence_refs=["ref1", "ref2"])
    assert seal.status == AdmissionEvidenceSealStatus.SEALED
    assert seal.sealed
    assert seal.immutable
    assert seal.seal_hash

    empty_seal = build_admission_evidence_seal()
    assert empty_seal.status == AdmissionEvidenceSealStatus.FAILED
    assert not empty_seal.sealed
