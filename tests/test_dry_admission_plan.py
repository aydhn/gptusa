from usa_signal_bot.paper_dry_admission.dry_admission_plan import build_default_dry_admission_plan, validate_dry_admission_plan_safety

def test_dry_admission_plan():
    plan = build_default_dry_admission_plan("cand1")
    assert plan.candidate_id == "cand1"
    assert not plan.execution_enabled
    assert plan.require_write_lock_refresh

    issues = validate_dry_admission_plan_safety(plan)
    assert len(issues) == 0
