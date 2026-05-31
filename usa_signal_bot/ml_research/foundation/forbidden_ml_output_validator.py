from typing import Any, Dict, List
from .ml_dataset_contract_builder import default_forbidden_ml_output_fields

def forbidden_ml_output_fields() -> List[str]:
    return default_forbidden_ml_output_fields()

def validate_no_forbidden_ml_output_fields(fields: List[str]) -> List[str]:
    forbidden = set(forbidden_ml_output_fields())
    errors = []
    for field in fields:
        if field in forbidden:
            errors.append(f"Forbidden field: {field}")
    return errors

def validate_no_forbidden_ml_output_in_payload(payload: Dict[str, Any]) -> List[str]:
    errors = []
    forbidden = set(forbidden_ml_output_fields())
    for key in payload.keys():
        if key in forbidden:
            errors.append(f"Forbidden key in payload: {key}")
    return errors

def validate_no_forbidden_ml_output_in_dataframe_columns(columns: List[str]) -> List[str]:
    return validate_no_forbidden_ml_output_fields(columns)

def forbidden_ml_output_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {"errors_count": len(errors)}

def forbidden_ml_output_validator_to_text(errors: List[str]) -> str:
    if errors:
        return f"Forbidden outputs found: {', '.join(errors)}"
    return "No forbidden outputs found"
