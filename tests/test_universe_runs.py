import pytest
import json
from usa_signal_bot.core.enums import ActiveUniverseSource, UniverseDataRunStatus, UniverseRunStep
from usa_signal_bot.data.universe_runs import (
    create_universe_data_run,
    start_universe_data_run,
    finish_universe_data_run,
    add_run_step_result,
    create_step_result,
    write_universe_data_run,
    read_universe_data_run,
    build_universe_run_dir
)

def test_universe_run_lifecycle(tmp_path):
    # Create
    run = create_universe_data_run(
        universe_name="test_uni",
        source=ActiveUniverseSource.DEFAULT_WATCHLIST,
        source_path="watchlist.csv",
        provider_name="yfinance",
        timeframes=["1d"],
        total_symbols=10
    )

    assert run.status == UniverseDataRunStatus.CREATED
    assert run.started_at_utc is None

    # Start
    run = start_universe_data_run(run)
    assert run.status == UniverseDataRunStatus.RUNNING
    assert run.started_at_utc is not None

    # Add step
    step = create_step_result(UniverseRunStep.RESOLVE_UNIVERSE, UniverseDataRunStatus.COMPLETED, "Done")
    run = add_run_step_result(run, step)
    assert len(run.steps) == 1

    # Finish
    run = finish_universe_data_run(run, UniverseDataRunStatus.COMPLETED)
    assert run.status == UniverseDataRunStatus.COMPLETED
    assert run.finished_at_utc is not None

    # I/O
    run_dir = build_universe_run_dir(tmp_path, run.run_id)
    meta_path = run_dir / "meta.json"
    write_universe_data_run(meta_path, run)

    assert meta_path.exists()

    loaded_run = read_universe_data_run(meta_path)
    assert loaded_run.run_id == run.run_id
    assert loaded_run.status == UniverseDataRunStatus.COMPLETED
    assert len(loaded_run.steps) == 1
    assert loaded_run.steps[0].step == UniverseRunStep.RESOLVE_UNIVERSE
