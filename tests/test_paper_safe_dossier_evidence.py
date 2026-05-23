from usa_signal_bot.paper_safe_dossier.dossier_evidence import collect_paper_safe_dossier_evidence, paper_safe_evidence_score
from usa_signal_bot.core.enums import PaperSafeDossierEvidenceStatus

def test_paper_safe_dossier_evidence():
    payload = {
        "review_id": "r1",
        "gates": [{"gate_id": "g1"}],
        "replay_results": [{"replay_result_id": "rr1"}],
        "integrity_audits": [{"audit_id": "a1"}],
        "rules": [{"rule_id": "ru1"}],
        "assertions": [{"assertion_id": "as1"}]
    }

    items = collect_paper_safe_dossier_evidence(payload)
    assert len(items) == 13

    # First 6 should be fresh
    for i in range(6):
        assert items[i].status == PaperSafeDossierEvidenceStatus.FRESH

    score = paper_safe_evidence_score(items)
    assert 0 < score < 100
