from pathlib import Path
def benchmark_comparison_store_dir(data_root: Path) -> Path:
    d = data_root / "backtesting" / "benchmark_comparison"
    d.mkdir(parents=True, exist_ok=True)
    return d
def benchmark_comparison_store_summary(data_root: Path) -> dict: return {"reviews_count": 0}
