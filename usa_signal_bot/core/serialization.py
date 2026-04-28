import json
from enum import Enum
from pathlib import Path
from typing import Any
import dataclasses

def serialize_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return enum_to_value(value)
    elif isinstance(value, Path):
        return str(value)
    elif dataclasses.is_dataclass(value):
        return dataclass_to_dict(value)
    elif isinstance(value, list):
        return [serialize_value(item) for item in value]
    elif isinstance(value, dict):
        return {str(k): serialize_value(v) for k, v in value.items()}
    return value

def enum_to_value(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    return value

def dataclass_to_dict(obj: Any) -> dict:
    if not dataclasses.is_dataclass(obj):
        raise TypeError("Object is not a dataclass.")

    result = {}
    for field in dataclasses.fields(obj):
        value = getattr(obj, field.name)
        result[field.name] = serialize_value(value)
    return result

def dataclass_to_json(obj: Any) -> str:
    return dict_to_json(dataclass_to_dict(obj))

def dict_to_json(data: dict) -> str:
    return json.dumps(serialize_value(data), sort_keys=True)
