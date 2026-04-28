from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone
from .serialization import dataclass_to_dict

def get_current_utc_string() -> str:
    return datetime.now(timezone.utc).isoformat()

@dataclass
class BaseDomainModel:
    created_at_utc: str = field(default_factory=get_current_utc_string)
    updated_at_utc: Optional[str] = None

    def to_dict(self) -> dict:
        return dataclass_to_dict(self)

    def validate(self) -> None:
        pass

@dataclass
class IdentifiedModel(BaseDomainModel):
    id: str = ""

    def validate(self) -> None:
        super().validate()
        from .model_validation import ensure_non_empty_string
        ensure_non_empty_string(self.id, "id")
