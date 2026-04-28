from typing import List, Dict

REQUIRED_UNIVERSE_COLUMNS = ["symbol", "asset_type"]
OPTIONAL_UNIVERSE_COLUMNS = ["name", "exchange", "currency", "active", "sector", "industry", "source", "notes"]
ALL_UNIVERSE_COLUMNS = REQUIRED_UNIVERSE_COLUMNS + OPTIONAL_UNIVERSE_COLUMNS
DEFAULT_CURRENCY = "USD"

def get_required_columns() -> List[str]:
    return REQUIRED_UNIVERSE_COLUMNS.copy()

def get_optional_columns() -> List[str]:
    return OPTIONAL_UNIVERSE_COLUMNS.copy()

def get_all_columns() -> List[str]:
    return ALL_UNIVERSE_COLUMNS.copy()

def validate_universe_columns(columns: List[str]) -> None:
    from usa_signal_bot.core.exceptions import UniverseValidationError
    missing = [c for c in REQUIRED_UNIVERSE_COLUMNS if c not in columns]
    if missing:
        raise UniverseValidationError(f"Missing required universe columns: {missing}")

def normalize_universe_row(row: Dict[str, str]) -> Dict[str, str]:
    normalized = row.copy()

    if not normalized.get("currency"):
        normalized["currency"] = DEFAULT_CURRENCY

    if "active" not in normalized or normalized["active"] == "":
        normalized["active"] = "true"

    if "asset_type" in normalized:
        normalized["asset_type"] = normalized["asset_type"].lower()

    return normalized
