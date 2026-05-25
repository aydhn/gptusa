
import json
from pathlib import Path
from typing import List, Dict, Any

def sample_macro_series_catalog_payloads() -> List[Dict[str, Any]]:
    return []

def sample_economic_event_payloads() -> List[Dict[str, Any]]:
    return []

def sample_earnings_event_payloads() -> List[Dict[str, Any]]:
    return []

def sample_corporate_action_payloads() -> List[Dict[str, Any]]:
    return []

def sample_news_metadata_payloads() -> List[Dict[str, Any]]:
    return []

def write_event_fixture_csv(path: Path, rows: List[Dict[str, Any]]) -> Path:
    import csv
    if not rows: return path
    with open(path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for r in rows: writer.writerow(r)
    return path

def write_event_fixture_json(path: Path, rows: List[Dict[str, Any]]) -> Path:
    with open(path, 'w') as f:
        json.dump(rows, f, indent=2)
    return path
