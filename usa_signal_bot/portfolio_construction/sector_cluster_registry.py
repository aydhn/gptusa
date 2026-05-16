import json
from pathlib import Path
from usa_signal_bot.portfolio_construction.portfolio_models import SectorClusterRecord
from usa_signal_bot.core.enums import SectorClusterSource

def load_sector_cluster_registry(path: Path) -> list[SectorClusterRecord]:
    if not path.exists():
        return []
    records = []
    try:
        if path.suffix == ".jsonl":
            with open(path, "r") as f:
                for line in f:
                    if not line.strip(): continue
                    data = json.loads(line)
                    records.append(SectorClusterRecord(
                        record_id=data.get("record_id", ""),
                        symbol=data.get("symbol", ""),
                        sector=data.get("sector"),
                        industry=data.get("industry"),
                        cluster=data.get("cluster"),
                        source=SectorClusterSource(data.get("source", "UNKNOWN")) if data.get("source") else SectorClusterSource.UNKNOWN,
                        confidence=data.get("confidence"),
                        notes=data.get("notes", []),
                        metadata=data.get("metadata", {})
                    ))
        else:
            with open(path, "r") as f:
                data_list = json.load(f)
            for data in data_list:
                records.append(SectorClusterRecord(
                    record_id=data.get("record_id", ""),
                    symbol=data.get("symbol", ""),
                    sector=data.get("sector"),
                    industry=data.get("industry"),
                    cluster=data.get("cluster"),
                    source=SectorClusterSource(data.get("source", "UNKNOWN")) if data.get("source") else SectorClusterSource.UNKNOWN,
                    confidence=data.get("confidence"),
                    notes=data.get("notes", []),
                    metadata=data.get("metadata", {})
                ))
    except Exception:
        pass
    return records

def write_sector_cluster_registry_example(path: Path) -> Path:
    from usa_signal_bot.portfolio_construction.portfolio_models import create_sector_cluster_record_id
    examples = [
        {"symbol": "AAPL", "sector": "technology", "industry": "hardware", "cluster": "mega_cap_tech", "source": "MANUAL_REGISTRY", "confidence": 100.0},
        {"symbol": "MSFT", "sector": "technology", "industry": "software", "cluster": "mega_cap_tech", "source": "MANUAL_REGISTRY", "confidence": 100.0},
        {"symbol": "NVDA", "sector": "technology", "industry": "semiconductors", "cluster": "ai_semis", "source": "MANUAL_REGISTRY", "confidence": 100.0},
        {"symbol": "XOM", "sector": "energy", "industry": "integrated_energy", "cluster": "energy", "source": "MANUAL_REGISTRY", "confidence": 90.0},
        {"symbol": "JPM", "sector": "financials", "industry": "banks", "cluster": "large_banks", "source": "MANUAL_REGISTRY", "confidence": 95.0},
        {"symbol": "UNH", "sector": "healthcare", "industry": "managed_care", "cluster": "healthcare", "source": "MANUAL_REGISTRY", "confidence": 90.0},
        {"symbol": "SPY", "sector": "broad_market", "industry": "etf", "cluster": "index_proxy", "source": "MANUAL_REGISTRY", "confidence": 90.0},
        {"symbol": "QQQ", "sector": "broad_market", "industry": "etf", "cluster": "growth_index_proxy", "source": "MANUAL_REGISTRY", "confidence": 90.0},
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump([
            {
                "record_id": create_sector_cluster_record_id(ex["symbol"]),
                **ex
            } for ex in examples
        ], f, indent=2)
    return path

def merge_sector_cluster_records(primary: list[SectorClusterRecord], secondary: list[SectorClusterRecord]) -> list[SectorClusterRecord]:
    merged = {}
    for r in secondary:
        merged[r.symbol] = r
    for r in primary:
        merged[r.symbol] = r
    return list(merged.values())

def sector_cluster_record_for_symbol(records: list[SectorClusterRecord], symbol: str) -> SectorClusterRecord | None:
    for r in records:
        if r.symbol == symbol:
            return r
    return None

def sector_cluster_registry_to_text(records: list[SectorClusterRecord], limit: int = 100) -> str:
    lines = [f"Sector Cluster Registry (Records: {len(records)})"]
    for i, r in enumerate(records[:limit]):
        lines.append(f"  {r.symbol}: sector={r.sector}, cluster={r.cluster}, source={r.source.value if hasattr(r.source, 'value') else str(r.source)}")
    if len(records) > limit:
        lines.append(f"  ... and {len(records) - limit} more.")
    lines.append("")
    lines.append("Note: Sector/cluster map is a local proxy and gives no official classification guarantees.")
    return "\n".join(lines)
