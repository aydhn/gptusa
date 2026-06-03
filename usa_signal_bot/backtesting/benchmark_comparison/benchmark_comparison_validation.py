from typing import Dict, Any
from dataclasses import dataclass, field
@dataclass
class BenchmarkComparisonValidationReport:
    valid: bool
def validate_no_sensitive_data_in_benchmark_payload(payload: Dict[str, Any]) -> BenchmarkComparisonValidationReport:
    return BenchmarkComparisonValidationReport(valid="api_key" not in str(payload).lower())
