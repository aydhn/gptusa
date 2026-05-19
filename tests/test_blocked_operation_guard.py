import pytest
from usa_signal_bot.core.enums import SandboxOperation, SandboxOperationDecision, SandboxRuntimeMode
from usa_signal_bot.core.exceptions import BlockedOperationGuardError
from usa_signal_bot.release_sandbox.sandbox_models import SandboxRuntimeContext
from usa_signal_bot.release_sandbox.blocked_operation_guard import (
    denied_operations_for_sandbox, sandbox_operation_decision,
    assert_operation_allowed, blocked_operation_guard_to_text
)

def test_denied_operations():
    denied = denied_operations_for_sandbox()
    assert SandboxOperation.SEND_ORDER in denied
    assert SandboxOperation.NETWORK_BROKER_CALL in denied

def test_operation_decisions():
    assert sandbox_operation_decision(SandboxOperation.SEND_ORDER) == SandboxOperationDecision.DENY
    assert sandbox_operation_decision(SandboxOperation.WRITE_SANDBOX_OUTPUT) == SandboxOperationDecision.ALLOW

    ctx = SandboxRuntimeContext(
        context_id="c1", created_at_utc="now", sandbox_id=None, bundle_id=None, bundle_version=None,
        runtime_mode=SandboxRuntimeMode.DRY_RUN_PREVIEW, in_memory_config={}, mounted_artifacts=[],
        sandbox_output_path=None, allowed_operations=[SandboxOperation.RUN_SIGNAL_PREVIEW], denied_operations=[],
        allowed_to_write_production_config=False, allowed_to_mutate_paper_state=False, allowed_to_send_orders=False,
        allowed_to_send_telegram_real=False, warnings=[], errors=[], metadata={}
    )

    assert sandbox_operation_decision(SandboxOperation.RUN_SIGNAL_PREVIEW, context=ctx) == SandboxOperationDecision.ALLOW

def test_assert_operation_allowed():
    with pytest.raises(BlockedOperationGuardError):
        assert_operation_allowed(SandboxOperation.SEND_ORDER)

    # Should not raise
    assert_operation_allowed(SandboxOperation.WRITE_SANDBOX_OUTPUT)
