from usa_signal_bot.paper_admission_review.no_write_continuity import validate_admission_no_write_continuity

def test_validate_admission_no_write_continuity():
    payload = {
        "activation_denied": True,
        "activation_allowed": False,
        "all_writes_blocked": True,
        "mutation_detected": False,
        "allows_active_paper": False,
        "allows_broker_execution": False,
        "allows_paper_state_mutation": False,
        "allows_config_patch": False,
        "allows_telegram_real_send": False
    }
    errors = validate_admission_no_write_continuity(payload)
    assert len(errors) == 0

    invalid_payload = {
        "activation_denied": False,
        "activation_allowed": True
    }
    errors = validate_admission_no_write_continuity(invalid_payload)
    assert len(errors) > 0
