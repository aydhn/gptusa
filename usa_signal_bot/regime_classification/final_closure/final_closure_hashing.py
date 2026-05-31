from typing import Any, Dict
import hashlib
import json
from usa_signal_bot.regime_classification.final_closure.phase135_models import (
    RegimeArtifactChainValidationResult,
    RegimeFinalClosureResult,
    MLInputContract
)

def stable_json_dumps(payload: Dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(',', ':'))

def compute_payload_hash(payload: Dict[str, Any]) -> str:
    text = stable_json_dumps(payload)
    return compute_text_hash(text)

def compute_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def compute_artifact_chain_hash(chain_validation: RegimeArtifactChainValidationResult) -> str:
    return compute_text_hash(chain_validation.validation_id)

def compute_closure_hash(closure_result: RegimeFinalClosureResult) -> str:
    return compute_text_hash(closure_result.closure_result_id)

def compute_freeze_seal_hash(seal_payload: Dict[str, Any]) -> str:
    return compute_payload_hash(seal_payload)

def compute_ml_input_contract_hash(contract: MLInputContract) -> str:
    return compute_text_hash(contract.contract_id)

def validate_hash_value(value: str | None) -> bool:
    return bool(value and len(value) == 64)
