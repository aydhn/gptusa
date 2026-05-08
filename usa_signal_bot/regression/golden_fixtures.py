from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List
import random
import hashlib
import json
from pathlib import Path
from usa_signal_bot.regression.regression_models import GoldenDatasetSpec
from usa_signal_bot.core.exceptions import GoldenFixtureError

def generate_deterministic_ohlcv_rows(symbol: str, start_date: str, row_count: int, base_price: float = 100.0) -> List[Dict[str, Any]]:
    # Use symbol and start_date to seed so we get deterministic but varying results
    seed_str = f"{symbol}_{start_date}"
    seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
    random.seed(seed)

    try:
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
    except ValueError:
        raise GoldenFixtureError(f"Invalid start_date format: {start_date}")

    rows = []
    current_price = base_price

    for i in range(row_count):
        # Deterministic random walk
        change_pct = random.uniform(-0.03, 0.03)
        open_p = current_price
        close_p = open_p * (1 + change_pct)

        # Ensure high >= max(open, close) and low <= min(open, close)
        high_p = max(open_p, close_p) * (1 + random.uniform(0.0, 0.02))
        low_p = min(open_p, close_p) * (1 - random.uniform(0.0, 0.02))

        volume = int(random.uniform(100000, 5000000))

        row = {
            "symbol": symbol,
            "timestamp": current_date.strftime("%Y-%m-%d"),
            "open": round(open_p, 4),
            "high": round(high_p, 4),
            "low": round(low_p, 4),
            "close": round(close_p, 4),
            "volume": volume
        }
        rows.append(row)

        current_price = close_p
        current_date += timedelta(days=1)
        # Skip weekends for realism, though deterministic
        while current_date.weekday() >= 5:
            current_date += timedelta(days=1)

    return rows

def generate_golden_ohlcv_dataset(symbols: List[str], start_date: str, row_count: int, timeframe: str = "1d") -> Dict[str, List[Dict[str, Any]]]:
    dataset = {}
    for i, sym in enumerate(sorted(symbols)):
        # Vary base price deterministically by symbol index
        base_price = 100.0 + (i * 10)
        dataset[sym] = generate_deterministic_ohlcv_rows(sym, start_date, row_count, base_price)
    return dataset

def generate_golden_signal_records(symbols: List[str], timeframe: str = "1d") -> List[Dict[str, Any]]:
    records = []
    for i, sym in enumerate(sorted(symbols)):
        seed_str = f"signal_{sym}_{timeframe}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)

        records.append({
            "signal_id": f"sig_{sym}_{timeframe}",
            "symbol": sym,
            "timeframe": timeframe,
            "action": random.choice(["BUY", "SELL", "HOLD"]),
            "confidence": round(random.uniform(0.3, 0.9), 2),
            "strategy": "golden_strategy",
            "timestamp": "2024-03-29"
        })
    return records

def generate_golden_candidate_records(symbols: List[str], timeframe: str = "1d") -> List[Dict[str, Any]]:
     records = []
     for i, sym in enumerate(sorted(symbols)):
        seed_str = f"candidate_{sym}_{timeframe}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)

        records.append({
            "candidate_id": f"cand_{sym}_{timeframe}",
            "symbol": sym,
            "score": round(random.uniform(50.0, 95.0), 2),
            "rank": i + 1,
            "timestamp": "2024-03-29"
        })
     return records

def generate_golden_risk_decision_records(symbols: List[str], timeframe: str = "1d") -> List[Dict[str, Any]]:
    records = []
    for i, sym in enumerate(sorted(symbols)):
        seed_str = f"risk_{sym}_{timeframe}"
        seed = int(hashlib.md5(seed_str.encode()).hexdigest(), 16) % (2**32)
        random.seed(seed)
        approved = random.choice([True, True, False])
        records.append({
            "decision_id": f"risk_{sym}_{timeframe}",
            "symbol": sym,
            "approved": approved,
            "reason": "golden_risk_rule" if not approved else "ok",
            "max_weight": 0.1 if approved else 0.0,
            "timestamp": "2024-03-29"
        })
    return records

def generate_golden_portfolio_allocation_records(symbols: List[str], timeframe: str = "1d") -> List[Dict[str, Any]]:
    records = []
    active_syms = sorted(symbols)[:max(1, len(symbols)//2)]
    weight = round(1.0 / len(active_syms), 4) if active_syms else 0.0

    for sym in active_syms:
        records.append({
            "allocation_id": f"alloc_{sym}_{timeframe}",
            "symbol": sym,
            "target_weight": weight,
            "timestamp": "2024-03-29"
        })
    return records

def write_golden_fixture_files(base_dir: Path, spec: GoldenDatasetSpec) -> Dict[str, str]:
    base_dir.mkdir(parents=True, exist_ok=True)
    paths = {}

    # OHLCV
    ohlcv_data = generate_golden_ohlcv_dataset(spec.symbols, spec.start_date, spec.row_count_per_symbol, spec.timeframe)
    for sym, rows in ohlcv_data.items():
        fname = f"ohlcv_{sym}_{spec.timeframe}.jsonl"
        fpath = base_dir / fname
        with open(fpath, "w") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")
        paths[f"ohlcv_{sym}"] = str(fpath)

    # Signals
    signals = generate_golden_signal_records(spec.symbols, spec.timeframe)
    sig_path = base_dir / "signals.jsonl"
    with open(sig_path, "w") as f:
        for sig in signals:
            f.write(json.dumps(sig) + "\n")
    paths["signals"] = str(sig_path)

    # Candidates
    candidates = generate_golden_candidate_records(spec.symbols, spec.timeframe)
    cand_path = base_dir / "candidates.jsonl"
    with open(cand_path, "w") as f:
        for cand in candidates:
            f.write(json.dumps(cand) + "\n")
    paths["candidates"] = str(cand_path)

    # Risk
    risk = generate_golden_risk_decision_records(spec.symbols, spec.timeframe)
    risk_path = base_dir / "risk_decisions.jsonl"
    with open(risk_path, "w") as f:
        for r in risk:
            f.write(json.dumps(r) + "\n")
    paths["risk_decisions"] = str(risk_path)

    # Portfolio
    allocations = generate_golden_portfolio_allocation_records(spec.symbols, spec.timeframe)
    alloc_path = base_dir / "allocations.jsonl"
    with open(alloc_path, "w") as f:
        for a in allocations:
            f.write(json.dumps(a) + "\n")
    paths["allocations"] = str(alloc_path)

    return paths

def calculate_fixture_checksum(payload: Any) -> str:
    # Stable checksum
    s = json.dumps(payload, sort_keys=True)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def golden_fixture_summary(base_dir: Path) -> Dict[str, Any]:
    if not base_dir.exists():
        return {"status": "missing"}

    files = list(base_dir.glob("*.jsonl"))
    return {
        "status": "exists",
        "file_count": len(files),
        "files": [f.name for f in files]
    }
