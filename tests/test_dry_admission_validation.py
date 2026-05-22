from usa_signal_bot.paper_dry_admission.dry_admission_validation import validate_no_live_execution_language_in_dry_admission

def test_dry_admission_validation():
    rep = validate_no_live_execution_language_in_dry_admission("this is a safe note")
    assert rep.valid

    rep_bad = validate_no_live_execution_language_in_dry_admission("sent to broker")
    assert not rep_bad.valid
