import pytest
from usa_signal_bot.app.runtime import initialize_runtime, run_startup_checks, build_runtime_summary
from usa_signal_bot.core.runtime_state import RuntimeContext

def test_initialize_runtime():
    context = initialize_runtime()
    assert isinstance(context, RuntimeContext)
    assert context.execution_mode == "local_paper_only"

    # Assert safe mode passes without raising RuntimeInitializationError
    context.assert_safe_mode()

def test_run_startup_checks():
    context = initialize_runtime()
    checks = run_startup_checks(context)
    assert isinstance(checks, list)
    assert "Config loaded and validated." in checks
    assert "Broker routing disabled." in checks
    assert "Web scraping disabled." in checks
    assert "Dashboard disabled." in checks

def test_build_runtime_summary():
    context = initialize_runtime()
    summary = build_runtime_summary(context)
    assert isinstance(summary, dict)
    assert summary["execution_mode"] == "local_paper_only"
    assert summary["safe_mode"]["broker_routing_disabled"] is True
