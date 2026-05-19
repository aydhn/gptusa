import pytest
from usa_signal_bot.core.enums import SandboxOperation, SandboxMountMode
from usa_signal_bot.release_sandbox.mount_planner import (
    build_read_only_mount_plan, mount_plan_to_text
)

def test_build_mount_plan():
    bundle_data = {
        "manifest": {"bundle_id": "b1", "bundle_version": "v1"}
    }
    plan = build_read_only_mount_plan(bundle_data, "src", "out")

    assert plan.bundle_id == "b1"
    assert plan.mount_mode == SandboxMountMode.READ_ONLY
    assert SandboxOperation.SEND_ORDER in plan.denied_operations
    assert SandboxOperation.WRITE_SANDBOX_OUTPUT in plan.allowed_operations
    assert SandboxOperation.WRITE_PRODUCTION_CONFIG in plan.denied_operations

    txt = mount_plan_to_text(plan)
    assert "READ_ONLY" in txt
