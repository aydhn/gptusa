"""Corporate action loader."""
import json
from pathlib import Path

from usa_signal_bot.core.enums import CorporateActionType, CorporateActionSource
from usa_signal_bot.core.exceptions import CorporateActionLoaderError
from usa_signal_bot.corporate_actions.corporate_action_models import CorporateActionEvent, create_corporate_action_event_id
from usa_signal_bot.providers.provider_models import ProviderResponse

def load_manual_corporate_actions_from_json(path: Path) -> list[CorporateActionEvent]:
    if not path.is_file():
        raise CorporateActionLoaderError(f"Manual corporate actions file not found: {path}")
    if ".." in str(path):
        raise CorporateActionLoaderError("Path traversal prevented.")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        events = []
        for item in data:
            action_type = CorporateActionType(item.get("action_type", "UNKNOWN"))
            events.append(CorporateActionEvent(
                event_id=item.get("event_id", create_corporate_action_event_id(item["symbol"], action_type, item["ex_date"])),
                symbol=item["symbol"],
                action_type=action_type,
                ex_date=item["ex_date"],
                value=item.get("value"),
                ratio_numerator=item.get("ratio_numerator"),
                ratio_denominator=item.get("ratio_denominator"),
                source=CorporateActionSource.MANUAL_FILE,
                confidence=item.get("confidence", 1.0),
                notes=item.get("notes", []),
                metadata=item.get("metadata", {})
            ))
        return events
    except Exception as e:
        raise CorporateActionLoaderError(f"Failed to load manual corporate actions from {path}: {e}")

def write_example_manual_corporate_actions(path: Path) -> Path:
    if ".." in str(path):
        raise CorporateActionLoaderError("Path traversal prevented.")
    path.parent.mkdir(parents=True, exist_ok=True)
    example_data = [
        {
            "symbol": "AAPL",
            "action_type": "SPLIT",
            "ex_date": "2020-08-31",
            "ratio_numerator": 4,
            "ratio_denominator": 1,
            "notes": ["Example 4-for-1 split"]
        },
        {
            "symbol": "MSFT",
            "action_type": "DIVIDEND",
            "ex_date": "2023-11-15",
            "value": 0.75,
            "notes": ["Example quarterly dividend"]
        }
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(example_data, f, indent=4)
    return path

def corporate_actions_from_provider_response(response: ProviderResponse) -> list[CorporateActionEvent]:
    # Placeholder for extracting actions from provider response metadata
    events = []

    if not response.metadata:
        return events

    for symbol, sym_meta in response.metadata.get("symbols", {}).items():
        # Example extracting splits
        for split in sym_meta.get("splits", []):
            events.append(CorporateActionEvent(
                event_id=create_corporate_action_event_id(symbol, CorporateActionType.SPLIT, split["date"]),
                symbol=symbol,
                action_type=CorporateActionType.SPLIT,
                ex_date=split["date"],
                value=None,
                ratio_numerator=split.get("numerator"),
                ratio_denominator=split.get("denominator"),
                source=CorporateActionSource.PROVIDER_METADATA,
                confidence=1.0,
                metadata={"provider_raw": split}
            ))

        # Example extracting dividends
        for div in sym_meta.get("dividends", []):
            events.append(CorporateActionEvent(
                event_id=create_corporate_action_event_id(symbol, CorporateActionType.DIVIDEND, div["date"]),
                symbol=symbol,
                action_type=CorporateActionType.DIVIDEND,
                ex_date=div["date"],
                value=div.get("amount"),
                ratio_numerator=None,
                ratio_denominator=None,
                source=CorporateActionSource.PROVIDER_METADATA,
                confidence=1.0,
                metadata={"provider_raw": div}
            ))

    return events

def corporate_actions_for_symbol(events: list[CorporateActionEvent], symbol: str) -> list[CorporateActionEvent]:
    return [e for e in events if e.symbol == symbol]

def filter_events_by_date_range(events: list[CorporateActionEvent], start_date: str | None, end_date: str | None) -> list[CorporateActionEvent]:
    filtered = []
    for e in events:
        if start_date and e.ex_date < start_date:
            continue
        if end_date and e.ex_date > end_date:
            continue
        filtered.append(e)
    return filtered

def corporate_action_events_to_text(events: list[CorporateActionEvent]) -> str:
    lines = [f"Corporate Actions ({len(events)}):"]
    for e in events:
        lines.append(f"  {e.symbol} {e.action_type.value if hasattr(e.action_type, 'value') else str(e.action_type)} on {e.ex_date} ({e.source.value if hasattr(e.source, 'value') else str(e.source)})")
        if e.value is not None:
            lines.append(f"    Value: {e.value}")
        if e.ratio_numerator is not None and e.ratio_denominator is not None:
            lines.append(f"    Ratio: {e.ratio_numerator}:{e.ratio_denominator}")
    return "\n".join(lines)
