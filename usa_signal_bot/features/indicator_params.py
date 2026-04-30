from dataclasses import dataclass, asdict
from typing import List, Any, Dict, Optional

from usa_signal_bot.core.exceptions import IndicatorParameterError

@dataclass
class IndicatorParameterSpec:
    name: str
    param_type: str
    default: Any
    required: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[Any]] = None
    description: Optional[str] = None

@dataclass
class IndicatorParameterSchema:
    indicator_name: str
    parameters: List[IndicatorParameterSpec]

def validate_parameter_schema(schema: IndicatorParameterSchema) -> None:
    if not schema.indicator_name:
        raise IndicatorParameterError("Schema indicator_name cannot be empty")
    names = set()
    for spec in schema.parameters:
        if not spec.name:
            raise IndicatorParameterError("Parameter name cannot be empty")
        if spec.name in names:
            raise IndicatorParameterError(f"Duplicate parameter name: {spec.name}")
        names.add(spec.name)
        if spec.param_type not in ("int", "float", "str", "bool"):
            raise IndicatorParameterError(f"Unsupported parameter type: {spec.param_type}")

def validate_indicator_params(schema: IndicatorParameterSchema, params: Dict[str, Any]) -> Dict[str, Any]:
    validated = {}
    specs = {spec.name: spec for spec in schema.parameters}

    for key, value in params.items():
        if key not in specs:
            raise IndicatorParameterError(f"Unknown parameter '{key}' for indicator '{schema.indicator_name}'")

        spec = specs[key]

        expected_type = {
            "int": int,
            "float": (int, float),
            "str": str,
            "bool": bool
        }[spec.param_type]

        if value is not None and not isinstance(value, expected_type):
            if spec.param_type == "bool" and not isinstance(value, bool):
                raise IndicatorParameterError(f"Parameter '{key}' must be of type {spec.param_type}, got {type(value).__name__}")
            elif spec.param_type != "bool" and isinstance(value, bool):
                raise IndicatorParameterError(f"Parameter '{key}' must be of type {spec.param_type}, got bool")
            elif not (spec.param_type in ("int", "float") and isinstance(value, (int, float))):
                raise IndicatorParameterError(f"Parameter '{key}' must be of type {spec.param_type}, got {type(value).__name__}")

        if value is not None:
            if spec.min_value is not None and value < spec.min_value:
                raise IndicatorParameterError(f"Parameter '{key}' value {value} is below minimum {spec.min_value}")
            if spec.max_value is not None and value > spec.max_value:
                raise IndicatorParameterError(f"Parameter '{key}' value {value} is above maximum {spec.max_value}")
            if spec.allowed_values is not None and value not in spec.allowed_values:
                raise IndicatorParameterError(f"Parameter '{key}' value {value} is not in allowed values {spec.allowed_values}")

        validated[key] = value

    for spec in schema.parameters:
        if spec.required and spec.name not in validated:
            if spec.default is not None:
                validated[spec.name] = spec.default
            else:
                raise IndicatorParameterError(f"Missing required parameter '{spec.name}' for indicator '{schema.indicator_name}'")
        elif spec.name not in validated:
            validated[spec.name] = spec.default

    return validated

def merge_params_with_defaults(schema: IndicatorParameterSchema, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = params or {}
    return validate_indicator_params(schema, params)

def parameter_schema_to_dict(schema: IndicatorParameterSchema) -> dict:
    return asdict(schema)
