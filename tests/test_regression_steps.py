import pytest
from pathlib import Path
from usa_signal_bot.regression.regression_steps import RegressionStepRunner
from usa_signal_bot.regression.regression_models import RegressionStepName, RegressionStepStatus
from usa_signal_bot.regression.golden_dataset import GoldenDatasetManager

def test_run_generate_golden_fixtures(tmp_path):
    runner = RegressionStepRunner(tmp_path)
    mgr = GoldenDatasetManager(tmp_path)
    context = {"dataset_spec": mgr.default_spec()}

    res = runner.run_step(RegressionStepName.GENERATE_GOLDEN_FIXTURES, context)
    assert res.status == RegressionStepStatus.PASSED
    assert len(res.output_paths) > 0

def test_run_load_golden_dataset(tmp_path):
    runner = RegressionStepRunner(tmp_path)
    mgr = GoldenDatasetManager(tmp_path)
    mgr.create_dataset(overwrite=True)

    context = {"dataset_name": "golden_small_us"}
    res = runner.run_step(RegressionStepName.LOAD_GOLDEN_DATASET, context)
    assert res.status == RegressionStepStatus.PASSED
    assert "dataset_spec" in context

def test_mock_pipeline_steps(tmp_path):
    runner = RegressionStepRunner(tmp_path)
    context = {}

    res = runner.run_step(RegressionStepName.DATA_CACHE_REHEARSAL, context)
    assert res.status == RegressionStepStatus.PASSED
    assert res.snapshot is not None

    res2 = runner.run_step(RegressionStepName.FEATURE_REHEARSAL, context)
    assert res2.status == RegressionStepStatus.PASSED
    assert res2.snapshot is not None

def test_run_notification_dry_run_rehearsal(tmp_path):
    runner = RegressionStepRunner(tmp_path)
    res = runner.run_step(RegressionStepName.NOTIFICATION_DRY_RUN_REHEARSAL, {})
    assert res.status == RegressionStepStatus.PASSED
    # Should not produce snapshot, just summary
    assert res.snapshot is None
