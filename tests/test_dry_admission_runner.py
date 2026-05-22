from usa_signal_bot.paper_dry_admission.dry_admission_plan import build_default_dry_admission_plan
from usa_signal_bot.paper_dry_admission.dry_admission_runner import PaperModeDryAdmissionRunner
from usa_signal_bot.core.enums import PaperModeDryAdmissionStatus

def test_dry_admission_runner():
    plan = build_default_dry_admission_plan("cand1")
    runner = PaperModeDryAdmissionRunner()
    run = runner.run_dry_admission(plan)

    assert run.candidate_id == "cand1"
    # Should be WARNING because human ledger has missing scopes by default
    assert run.status == PaperModeDryAdmissionStatus.WARNING or run.status == PaperModeDryAdmissionStatus.COMPLETED_NO_WRITE
    assert not run.mutation_detected
    assert run.all_writes_blocked
