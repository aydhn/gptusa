"""One local, human-approved learning cycle (research only; nothing is ever activated).

refresh (optional, only on request) -> feature drift (PSI) -> retrain trigger -> [if triggered] CPCV tree candidate
-> registry CPCV+DSR+SPA gate -> markdown + JSON report. A file lock and an idempotency record make a second run on
the same day a no-op unless ``force``. Promotion happens only through ``ml-loop-approve`` (a named human).
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from usa_signal_bot.core.enums import IdempotencyStatus, LockAcquisitionMode, RunLockScope
from usa_signal_bot.scheduler.atomic_io import atomic_write_json, atomic_write_text
from usa_signal_bot.scheduler.duplicate_run_guard import build_idempotency_key, build_run_payload_checksum, check_duplicate_run
from usa_signal_bot.scheduler.lock_manager import FileRunLockManager
from usa_signal_bot.scheduler.run_identity import create_run_identity
from usa_signal_bot.scheduler.scheduler_models import IdempotencyRecord

NOTICE = "Araştırma çıktısıdır, yatırım tavsiyesi değildir. activation: none (aktivasyon yok; yalnız `ml-loop-approve` ile insan onayı)."
SCOPE = RunLockScope.GLOBAL


@dataclass
class CycleConfig:
    source: str = "csv"  # csv | synthetic
    csv_dir: Optional[str] = None
    memberships: Optional[str] = None
    seed: int = 7
    model: str = "hgb"
    meta: bool = False
    trials: int = 1
    hypothesis_log: Optional[str] = None
    commission_bps: float = 1.0
    slippage_bps: float = 5.0
    cash_rate: float = 0.02
    registry_dir: str = "data/model_registry"
    out_dir: Optional[str] = None
    refresh: bool = False
    refresh_start: str = "2010-01-01"
    force: bool = False
    train_anyway: bool = False  # train a candidate even if drift did not trigger (still gated, still not activated)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _load_data(cfg: CycleConfig):
    from usa_signal_bot.evidence.data import load_csv_market, synthetic_market

    if cfg.source == "csv":
        if not cfg.csv_dir:
            raise ValueError("--csv-dir is required with --source csv")
        return load_csv_market(cfg.csv_dir, cfg.memberships)
    return synthetic_market(seed=cfg.seed)


def _read_record(path: Path) -> Optional[IdempotencyRecord]:
    if not path.exists():
        return None
    d = json.loads(path.read_text(encoding="utf-8"))
    d["scope"], d["status"] = RunLockScope(d["scope"]), IdempotencyStatus(d["status"])
    return IdempotencyRecord(**d)


def _write_record(path: Path, rec: IdempotencyRecord) -> None:
    d = asdict(rec)
    d["scope"], d["status"] = rec.scope.value, rec.status.value
    atomic_write_json(path, d)


def render_markdown(rep: Dict[str, Any]) -> str:
    lines = [f"# ML döngü raporu ({rep['date']})", "", f"> {NOTICE}", "",
             f"- Veri: {rep['data_label']} | gün sayısı: {rep['n_days']}",
             f"- Drift tetik: **{rep['drift']['triggered']}** (maks. PSI {rep['drift']['max_psi']:.3f})"]
    lines += [f"  - {r}" for r in rep["drift"]["reasons"][:5]]
    c = rep.get("candidate")
    if c:
        m = c["metrics"]
        lines += [f"- Aday: `{c['model_id']}` durum **{c['status']}** (N deneme={c['n_trials']})",
                  f"  - CPCV yol medyan CAGR {m['median_path_cagr']:.1%} vs kıyas {m['bench_cagr']:.1%}; "
                  f"medyan aşırı Sharpe {m['median_path_excess_sharpe']:.2f}; pozitif yol {m['positive_path_fraction']:.0%}",
                  f"  - DSR(excess) {m['dsr_excess']:.2f}, SPA p {m['spa_p']:.3f}, sızıntı temiz={c['leakage_clean']}"]
        lines += [f"  - kapı: {r}" for r in c["gate_reasons"]]
    else:
        lines.append("- Aday eğitilmedi (drift tetiklemedi).")
    lines += [f"- Veri yenileme: {rep['refresh']}", "- activation: none", "- activation_allowed: False",
              "- Terfi yalnız mevcut `ml-loop-approve` ile, adı belli bir insan tarafından yapılır.", ""]
    return "\n".join(lines)


def run_cycle(cfg: CycleConfig, clock: Callable[[], datetime] = _utc_now, data=None,
              trainer: Optional[Callable[..., Any]] = None, fetcher: Optional[Callable[[], Any]] = None) -> Dict[str, Any]:
    """Run one cycle. Returns the report dict; ``status`` is ``done``, ``skipped_duplicate`` or ``locked``."""
    now = clock()
    date = now.strftime("%Y-%m-%d")
    out = Path(cfg.out_dir) if cfg.out_dir else Path("data/ml_cycle") / date
    out.mkdir(parents=True, exist_ok=True)
    payload = {"date": date, "source": cfg.source, "csv_dir": cfg.csv_dir, "seed": cfg.seed, "model": cfg.model, "meta": cfg.meta}
    key = build_idempotency_key(SCOPE, payload)
    rec_path = out / "idempotency.json"
    rec = _read_record(rec_path)
    if rec and not cfg.force and check_duplicate_run([rec], SCOPE, payload).duplicate:
        return {"status": "skipped_duplicate", "date": date, "out_dir": str(out), "message": "same-day cycle already ran; use --force"}

    mgr = FileRunLockManager(out / ".locks")
    ident = create_run_identity(SCOPE, owner="ml-loop-cycle", idempotency_key=key)
    got = mgr.acquire(SCOPE, ident, mode=LockAcquisitionMode.FAIL_FAST)
    if not got.acquired:
        return {"status": "locked", "date": date, "out_dir": str(out), "message": "; ".join(got.errors)}
    checksum = build_run_payload_checksum(payload)
    try:
        _write_record(rec_path, IdempotencyRecord(key, ident.run_id, SCOPE, IdempotencyStatus.IN_PROGRESS, now.isoformat(),
                                                  payload_checksum=checksum))
        rep = _run_locked(cfg, now, date, out, data, trainer, fetcher)
        _write_record(rec_path, IdempotencyRecord(key, ident.run_id, SCOPE, IdempotencyStatus.COMPLETED_BEFORE, now.isoformat(),
                                                  completed_at_utc=clock().isoformat(), payload_checksum=checksum,
                                                  output_paths={"json": str(out / "cycle_report.json"), "md": str(out / "cycle_report.md")}))
        return rep
    except Exception:
        rec_path.unlink(missing_ok=True)  # a failed run must not block a retry
        raise
    finally:
        mgr.release(got.lock, ident)


def _run_locked(cfg, now, date, out, data, trainer, fetcher) -> Dict[str, Any]:
    from usa_signal_bot.evidence.costs import CostModel
    from usa_signal_bot.evidence.universe import PointInTimeUniverse
    from usa_signal_bot.ml_loop.drift import feature_drift
    from usa_signal_bot.ml_loop.registry import CpcvThresholds, ModelRegistry
    from usa_signal_bot.ml_loop.retrain_trigger import evaluate_retrain
    from usa_signal_bot.ml_loop.tree_cpcv import build_features, run_tree_cpcv

    refresh = "yok (mevcut CSV kullanıldı)"
    if cfg.refresh:
        if not cfg.csv_dir:
            raise ValueError("--refresh needs --csv-dir")
        if fetcher is None:
            from usa_signal_bot.evidence.fetch import DEFAULT_TICKERS, fetch_daily

            def fetcher():
                return fetch_daily(DEFAULT_TICKERS, cfg.csv_dir, start=cfg.refresh_start)
        fetcher()
        refresh = "evidence/fetch.py ile yenilendi (yfinance, günlük önbellek)"
    data = data if data is not None else _load_data(cfg)
    prices = data.prices
    members = PointInTimeUniverse.from_frame(data.memberships).membership_matrix(prices.index, prices.columns)

    x, _ = build_features(prices, members, 5)
    half = len(x) // 2
    results = feature_drift(x.iloc[:half], x.iloc[half:])
    req = evaluate_retrain(results)
    psis = [r.psi for r in results if r.psi == r.psi]
    rep: Dict[str, Any] = {
        "status": "done", "date": date, "generated_at_utc": now.isoformat(), "out_dir": str(out), "data_label": data.label,
        "n_days": int(len(prices)), "refresh": refresh, "activation": "none", "activation_allowed": False,
        "drift": {"triggered": req.triggered, "reasons": req.reasons, "max_psi": max(psis) if psis else 0.0,
                  "psi": {r.metric_name: r.psi for r in results}},
        "candidate": None, "notice": NOTICE,
    }
    if req.triggered or cfg.train_anyway:
        hlog = None
        if cfg.hypothesis_log:
            from usa_signal_bot.evidence.hypothesis_log import HypothesisLog

            hlog = HypothesisLog(Path(cfg.hypothesis_log), clock=lambda: now.isoformat())
        n_trials = (hlog.n_trials(data.label) + 1) if hlog else cfg.trials
        var_sr = hlog.sharpe_variance(data.label) if hlog and hlog.n_trials(data.label) > 1 else None
        run = trainer or run_tree_cpcv
        res = run(prices, members, CostModel(cfg.commission_bps, cfg.slippage_bps), cfg.cash_rate, kind=cfg.model,
                  meta_labeling=cfg.meta, n_trials=n_trials, var_sr_trials=var_sr, seed=cfg.seed)
        if hlog:
            med = float(sorted(res.path_sharpe)[len(res.path_sharpe) // 2]) / (252 ** 0.5)
            hlog.append(f"ml-cycle-{date}", f"ML {cfg.model}{' +meta' if cfg.meta else ''}", {"top_frac": 0.3}, len(prices), med, data.label)
        model_id = f"cycle_{date}_{cfg.model}{'_meta' if cfg.meta else ''}_{now.strftime('%H%M%S')}"
        reg = ModelRegistry(Path(cfg.registry_dir), lambda: now.strftime("%Y-%m-%dT%H:%M:%SZ"))
        reg.register(model_id, {"model": float(cfg.model == "rf"), "meta": float(cfg.meta)}, res.metrics(), res.fingerprint, res.leakage_clean)
        got = reg.evaluate_cpcv_promotion(model_id, CpcvThresholds())
        rep["candidate"] = {"model_id": model_id, "status": got.status, "gate_reasons": list(got.gate_reasons), "metrics": got.metrics,
                            "leakage_clean": bool(res.leakage_clean), "n_trials": n_trials, "activation_allowed": got.activation_allowed}
    atomic_write_json(out / "cycle_report.json", rep)
    atomic_write_text(out / "cycle_report.md", render_markdown(rep))
    return rep
