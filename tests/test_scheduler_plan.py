from usa_signal_bot.scheduler.scheduler_plan import (
    default_scheduler_jobs, build_scheduler_plan, validate_scheduler_dependencies,
    topological_sort_jobs, scheduler_plan_to_text
)
from usa_signal_bot.core.enums import SchedulerPlanStatus

def test_default_scheduler_jobs():
    jobs = default_scheduler_jobs()
    assert len(jobs) > 0

def test_build_scheduler_plan():
    plan = build_scheduler_plan(dry_run=True)
    assert plan.status == SchedulerPlanStatus.CREATED
    assert plan.dry_run is True
    assert len(plan.jobs) > 0

def test_validate_scheduler_dependencies():
    jobs = default_scheduler_jobs()
    valid, warnings, errors = validate_scheduler_dependencies(jobs)
    assert valid is True

    # Introduce bad dep
    jobs[0].depends_on = ["non_existent_job"]
    valid, warnings, errors = validate_scheduler_dependencies(jobs)
    assert valid is False
    assert len(errors) > 0

def test_topological_sort():
    jobs = default_scheduler_jobs()
    sorted_jobs = topological_sort_jobs(jobs)
    assert len(sorted_jobs) == len(jobs)

def test_scheduler_plan_to_text():
    plan = build_scheduler_plan()
    txt = scheduler_plan_to_text(plan)
    assert "Scheduler Plan" in txt
