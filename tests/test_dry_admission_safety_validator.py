from usa_signal_bot.paper_dry_admission.dry_admission_plan import build_default_dry_admission_plan
from usa_signal_bot.paper_dry_admission.dry_admission_safety_validator import validate_dry_admission_safety

def test_dry_admission_safety_validator():
    plan = build_default_dry_admission_plan()
    issues = validate_dry_admission_safety(plan=plan)
    assert len(issues) == 0

    plan.active_paper_enabled = True
    issues_bad = validate_dry_admission_safety(plan=plan)
    assert len(issues_bad) > 0
