import pytest
from pathlib import Path
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxRuntimeMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan, ReleaseSandboxReview
from usa_signal_bot.release_sandbox.sandbox_store import (
    sandbox_store_dir, write_sandbox_activation_plan_json,
    write_release_sandbox_review_json, read_release_sandbox_review_json,
    list_release_sandbox_reviews, get_latest_release_sandbox_review
)

def test_sandbox_store(tmp_path):
    d = sandbox_store_dir(tmp_path)
    assert d.exists()

    plan = SandboxActivationPlan("a1", "now", "b1", "v1", SandboxActivationStatus.VALIDATED, None, {}, {}, {}, SandboxRuntimeMode.DRY_RUN_PREVIEW, False, False, False, False, [], [])
    p_path = d / "plan.json"
    write_sandbox_activation_plan_json(p_path, plan)
    assert p_path.exists()

    review = ReleaseSandboxReview("rev1", "now", "FULL_SANDBOX_REVIEW", [], [], [], [], {}, [], [])
    r_path = d / "rev.json"
    write_release_sandbox_review_json(r_path, review)

    # Needs to match folder pattern for glob to work if strictly tested,
    # but we can check simple read works
    data = read_release_sandbox_review_json(r_path)
    assert data["review_id"] == "rev1"
