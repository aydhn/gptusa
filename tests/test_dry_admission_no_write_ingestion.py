from usa_signal_bot.paper_dry_admission.no_write_ingestion import (
    ingest_no_write_admission_full_review,
    extract_no_write_contract,
    extract_activation_replay_result,
    extract_paper_mode_preflight,
    no_write_supports_dry_admission
)

def test_no_write_ingestion():
    payload = {
        "contracts": [{"contract_id": "c1", "activation_denied": True, "activation_allowed": False}],
        "replays": [{"replay_id": "r1"}],
        "preflights": [{"preflight_id": "p1", "decision": "PASS_NO_WRITE_PREFLIGHT", "mutation_detected": False, "all_writes_blocked": True, "activation_allowed": False}]
    }

    contract = extract_no_write_contract(payload)
    assert contract["contract_id"] == "c1"

    supported, reasons = no_write_supports_dry_admission(payload)
    assert supported is True
    assert len(reasons) == 0
