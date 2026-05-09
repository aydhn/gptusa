import pytest
from pathlib import Path
import json

def test_retention_store_dirs(tmp_path):
    from usa_signal_bot.retention.retention_store import (
        cleanup_plans_dir, cleanup_results_dir, quota_reports_dir, audit_dir
    )
    assert cleanup_plans_dir(tmp_path).name == "plans"
    assert cleanup_results_dir(tmp_path).name == "results"
    assert quota_reports_dir(tmp_path).name == "quota"
    assert audit_dir(tmp_path).name == "audit"

def test_write_read_plan(tmp_path):
    from usa_signal_bot.retention.retention_models import CleanupPlan
    from usa_signal_bot.retention.retention_store import write_cleanup_plan_json, read_cleanup_plan_json

    plan = CleanupPlan(
        plan_id="test_plan",
        created_at_utc="now",
        dry_run=True,
        candidates=[],
        total_candidate_count=0,
        total_candidate_size_bytes=0,
        protected_count=0,
        delete_candidate_count=0,
        review_required_count=0,
        warnings=[],
        errors=[]
    )

    path = tmp_path / "plan.json"
    write_cleanup_plan_json(path, plan)

    data = read_cleanup_plan_json(path)
    assert data["plan_id"] == "test_plan"
    assert data["dry_run"] is True
