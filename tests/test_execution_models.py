import pytest
from usa_signal_bot.core.enums import ResearchRunType, ExperimentExecutionMode, ResearchRunStatus
from usa_signal_bot.research_execution.execution_models import (
    ConfigSnapshot, ExperimentRunContext, ResearchRun,
    validate_experiment_run_context, validate_config_snapshot, create_config_snapshot_id
)
from usa_signal_bot.core.exceptions import ResearchExecutionValidationError

def test_config_snapshot_validation_blocks_secrets():
    payload = {"api_key": "mysecret"}
    snap = ConfigSnapshot(
        snapshot_id=create_config_snapshot_id(),
        created_at_utc="now",
        snapshot_type=ResearchRunType.BASELINE,
        config_hash="abc",
        config_payload=payload,
        source_ref=None,
        warnings=[], errors=[], metadata={}
    )
    with pytest.raises(ResearchExecutionValidationError):
        validate_config_snapshot(snap)

def test_config_snapshot_allows_redacted_secrets():
    payload = {"api_key": "[REDACTED]"}
    snap = ConfigSnapshot(
        snapshot_id=create_config_snapshot_id(),
        created_at_utc="now",
        snapshot_type=ResearchRunType.BASELINE,
        config_hash="abc",
        config_payload=payload,
        source_ref=None,
        warnings=[], errors=[], metadata={}
    )
    validate_config_snapshot(snap)

def test_run_context_blocks_live_settings():
    ctx = ExperimentRunContext(
        context_id="ctx_1",
        created_at_utc="now",
        experiment_id=None, hypothesis_id=None,
        run_type=ResearchRunType.BASELINE,
        execution_mode=ExperimentExecutionMode.MOCK_ONLY,
        config_snapshot=None, validation_plan={}, acceptance_gates=[], data_scope={},
        allowed_to_modify_config=True,
        allowed_to_send_orders=False,
        warnings=[], errors=[]
    )
    with pytest.raises(ResearchExecutionValidationError):
        validate_experiment_run_context(ctx)
