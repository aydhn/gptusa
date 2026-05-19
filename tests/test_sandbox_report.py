import pytest
from usa_signal_bot.core.enums import SandboxActivationStatus, SandboxRuntimeMode
from usa_signal_bot.release_sandbox.sandbox_models import SandboxActivationPlan
from usa_signal_bot.release_sandbox.sandbox_report import (
    build_sandbox_review, sandbox_review_summary, sandbox_report_to_text
)

def test_build_sandbox_review():
    plan = SandboxActivationPlan(
        "a1", "now", "b1", "v1", SandboxActivationStatus.VALIDATED, None, {}, {}, {}, SandboxRuntimeMode.DRY_RUN_PREVIEW,
        False, False, False, False, [], []
    )

    review = build_sandbox_review(plan)
    assert review.report_type == "FULL_SANDBOX_REVIEW"
    assert len(review.activation_plans) == 1

    s = sandbox_review_summary(review)
    assert s["activation_plans_count"] == 1

    txt = sandbox_report_to_text(review)
    assert "LIMITATIONS" in txt
    assert "not investment advice" in txt
