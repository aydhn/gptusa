from usa_signal_bot.paper_admission_review.write_lock_integration import validate_write_lock_refresh_for_admission_review

def test_validate_write_lock_refresh_for_admission_review():
    payload = {
        "write_lock_refresh": {
            "all_writes_blocked": True,
            "mutation_detected": False,
            "unblocked_write_attempt_count": 0,
            "hash_unchanged": True,
            "allows_active_paper": False,
            "allows_broker_execution": False,
            "allows_paper_state_mutation": False,
            "allows_config_patch": False,
            "allows_telegram_real_send": False
        }
    }
    errors = validate_write_lock_refresh_for_admission_review(payload)
    assert len(errors) == 0

    invalid_payload = {
        "write_lock_refresh": {
            "all_writes_blocked": False,
            "unblocked_write_attempt_count": 1
        }
    }
    errors = validate_write_lock_refresh_for_admission_review(invalid_payload)
    assert len(errors) > 0
