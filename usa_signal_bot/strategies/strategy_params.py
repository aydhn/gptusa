from dataclasses import dataclass, field
from typing import Any, List, Optional, Dict
from usa_signal_bot.core.exceptions import StrategyParameterError

@dataclass
class StrategyParameterSpec:
    name: str
    param_type: str
    default: Any
    required: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    allowed_values: Optional[List[Any]] = None
    description: Optional[str] = None

@dataclass
class StrategyParameterSchema:
    strategy_name: str
    parameters: List[StrategyParameterSpec]

def validate_strategy_parameter_schema(schema: StrategyParameterSchema) -> None:
    if not schema.strategy_name:
        raise StrategyParameterError("strategy_name cannot be empty")

    names = set()
    for param in schema.parameters:
        if not param.name:
            raise StrategyParameterError("Parameter name cannot be empty")
        if param.name in names:
            raise StrategyParameterError(f"Duplicate parameter name: {param.name}")
        names.add(param.name)

        if param.param_type not in ["int", "float", "str", "bool"]:
            raise StrategyParameterError(f"Unsupported parameter type: {param.param_type} for {param.name}")

def merge_strategy_params_with_defaults(schema: StrategyParameterSchema, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    merged = {}
    params = params or {}

    for spec in schema.parameters:
        if spec.name in params:
            merged[spec.name] = params[spec.name]
        else:
            merged[spec.name] = spec.default

    return merged

def validate_strategy_params(schema: StrategyParameterSchema, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    params = params or {}
    merged = merge_strategy_params_with_defaults(schema, params)

    for spec in schema.parameters:
        if spec.required and merged.get(spec.name) is None:
            raise StrategyParameterError(f"Required parameter missing: {spec.name}")

        val = merged.get(spec.name)
        if val is None:
            continue

        if spec.param_type == "int" and not isinstance(val, int):
            raise StrategyParameterError(f"Parameter {spec.name} must be int, got {type(val)}")
        elif spec.param_type == "float" and not isinstance(val, (int, float)):
            raise StrategyParameterError(f"Parameter {spec.name} must be float, got {type(val)}")
        elif spec.param_type == "str" and not isinstance(val, str):
            raise StrategyParameterError(f"Parameter {spec.name} must be str, got {type(val)}")
        elif spec.param_type == "bool" and not isinstance(val, bool):
            raise StrategyParameterError(f"Parameter {spec.name} must be bool, got {type(val)}")

        if isinstance(val, (int, float)):
            if spec.min_value is not None and val < spec.min_value:
                raise StrategyParameterError(f"Parameter {spec.name} value {val} is below minimum {spec.min_value}")
            if spec.max_value is not None and val > spec.max_value:
                raise StrategyParameterError(f"Parameter {spec.name} value {val} is above maximum {spec.max_value}")

        if spec.allowed_values is not None and val not in spec.allowed_values:
            raise StrategyParameterError(f"Parameter {spec.name} value {val} not in allowed values: {spec.allowed_values}")

    for key in params:
        if not any(p.name == key for p in schema.parameters):
            raise StrategyParameterError(f"Unknown parameter: {key} for strategy {schema.strategy_name}")

    return merged

def strategy_parameter_schema_to_dict(schema: StrategyParameterSchema) -> dict:
    return {
        "strategy_name": schema.strategy_name,
        "parameters": [
            {
                "name": p.name,
                "param_type": p.param_type,
                "default": p.default,
                "required": p.required,
                "min_value": p.min_value,
                "max_value": p.max_value,
                "allowed_values": p.allowed_values,
                "description": p.description
            } for p in schema.parameters
        ]
    }

# --- Helpers for Parameter Sensitivity & Grid ---

def get_parameter_spec(schema: StrategyParameterSchema, name: str) -> StrategyParameterSpec | None:
    for spec in schema.parameters:
        if spec.name == name:
            return spec
    return None

def strategy_schema_parameter_names(schema: StrategyParameterSchema) -> list[str]:
    return [spec.name for spec in schema.parameters]

def is_parameter_value_allowed(spec: StrategyParameterSpec, value: Any) -> bool:
    if spec.allowed_values and value not in spec.allowed_values:
        return False
    if spec.min_value is not None and value < spec.min_value:
        return False
    if spec.max_value is not None and value > spec.max_value:
        return False
    return True

def coerce_parameter_value(value: Any, param_type: str) -> Any:
    if param_type == "int":
        return int(value)
    elif param_type == "float":
        return float(value)
    elif param_type == "bool":
        if isinstance(value, str):
            return value.lower() in ("true", "1", "yes")
        return bool(value)
    elif param_type == "str":
        return str(value)
    return value
