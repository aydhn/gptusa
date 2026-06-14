import json
from pathlib import Path
from typing import Any
import dataclasses
from usa_signal_bot.core.serialization import to_dict_clean, serialize_value


def write_diagnostic_review_json(path: Path, item: Any) -> Path:
    data = (
        to_dict_clean(item) if dataclasses.is_dataclass(item) else serialize_value(item)
    )
    path.write_text(json.dumps(data, indent=2))
    return path
