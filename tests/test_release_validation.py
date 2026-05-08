from usa_signal_bot.release.release_validation import validate_no_live_execution_language_in_release

def test_no_live_language():
    res1 = validate_no_live_execution_language_in_release("This is a test runbook.")
    assert res1.valid is True

    res2 = validate_no_live_execution_language_in_release("This release is live approved.")
    assert res2.valid is False
    assert "live approved" in res2.errors[0]
