import json
from datetime import datetime, timezone

import pytest

from usa_signal_bot.evidence.data import synthetic_market
from usa_signal_bot.ml_loop.auto_cycle import CycleConfig, run_cycle
from usa_signal_bot.ml_loop.tree_cpcv import CPCVModelResult


def _clock(day=10, hour=6):
    return lambda: datetime(2026, 10, day, hour, 0, 0, tzinfo=timezone.utc)


def _fake_trainer(calls):
    def trainer(prices, members, cost, cash_rate, **kw):
        calls.append(kw)
        return CPCVModelResult("hgb", False, 3, [0.1] * 3, [1.0] * 3, [0.2] * 3, 0.1, 1.0, dsr_excess=0.5, spa_p=0.4,
                               leakage_clean=True, n_trials=kw["n_trials"], fingerprint="fp")
    return trainer


@pytest.fixture(scope="module")
def market():
    return synthetic_market(seed=3, n_symbols=12, n_days=700)


def _cfg(tmp_path, **kw):
    return CycleConfig(source="synthetic", out_dir=str(tmp_path / "out"), registry_dir=str(tmp_path / "reg"), train_anyway=True, **kw)


def test_cycle_trains_gates_and_never_activates(tmp_path, market):
    calls = []
    rep = run_cycle(_cfg(tmp_path), _clock(), data=market, trainer=_fake_trainer(calls))
    assert rep["status"] == "done" and len(calls) == 1
    c = rep["candidate"]
    assert c["status"] == "REJECTED" and c["activation_allowed"] is False and rep["activation"] == "none"
    out = tmp_path / "out"
    assert json.loads((out / "cycle_report.json").read_text(encoding="utf-8"))["activation_allowed"] is False
    md = (out / "cycle_report.md").read_text(encoding="utf-8")
    assert "activation: none" in md and "yatırım tavsiyesi değildir" in md


def test_second_run_same_day_is_noop_unless_force(tmp_path, market):
    calls = []
    run_cycle(_cfg(tmp_path), _clock(), data=market, trainer=_fake_trainer(calls))
    again = run_cycle(_cfg(tmp_path), _clock(hour=9), data=market, trainer=_fake_trainer(calls))
    assert again["status"] == "skipped_duplicate" and len(calls) == 1
    forced = run_cycle(_cfg(tmp_path, force=True), _clock(hour=9), data=market, trainer=_fake_trainer(calls))
    assert forced["status"] == "done" and len(calls) == 2


def test_no_training_without_drift_trigger(tmp_path, market):
    calls = []
    cfg = CycleConfig(source="synthetic", out_dir=str(tmp_path / "o"), registry_dir=str(tmp_path / "r"))
    rep = run_cycle(cfg, _clock(), data=market, trainer=_fake_trainer(calls))
    assert rep["status"] == "done" and (rep["candidate"] is None) == (not rep["drift"]["triggered"])
    assert len(calls) == (1 if rep["drift"]["triggered"] else 0)


def test_refresh_only_when_requested(tmp_path, market):
    fetched = []
    run_cycle(_cfg(tmp_path / "a"), _clock(), data=market, trainer=_fake_trainer([]), fetcher=lambda: fetched.append(1))
    assert not fetched
    run_cycle(_cfg(tmp_path / "b", csv_dir=str(tmp_path), refresh=True), _clock(), data=market, trainer=_fake_trainer([]),
              fetcher=lambda: fetched.append(1))
    assert fetched == [1]


def test_failed_run_does_not_block_retry(tmp_path, market):
    def boom(*a, **k):
        raise RuntimeError("x")
    with pytest.raises(RuntimeError):
        run_cycle(_cfg(tmp_path), _clock(), data=market, trainer=boom)
    assert run_cycle(_cfg(tmp_path), _clock(), data=market, trainer=_fake_trainer([]))["status"] == "done"


def test_cli_registered_once():
    import argparse

    from usa_signal_bot.ml_loop.cli import setup_ml_loop_cli

    p = argparse.ArgumentParser()
    setup_ml_loop_cli(p.add_subparsers())
    assert p.parse_args(["ml-loop-cycle", "--source", "synthetic"]).force is False
