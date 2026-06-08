from pathlib import Path
from typing import Any, Dict
import json
from usa_signal_bot.portfolio.construction.phase155_models import (
    SizingPrototypeIngestionResult
)
from usa_signal_bot.core.exceptions import SizingPrototypeArtifactLoaderError

def load_sizing_prototype_artifacts(ingestion: SizingPrototypeIngestionResult) -> Dict[str, Any]:
    if not ingestion.source_path:
        return {}

    try:
        with open(ingestion.source_path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise SizingPrototypeArtifactLoaderError(f"Failed to load artifacts from {ingestion.source_path}: {e}")
