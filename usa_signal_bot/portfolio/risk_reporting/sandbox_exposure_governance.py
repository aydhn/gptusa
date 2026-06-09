from typing import Any, Dict, List
import datetime

from usa_signal_bot.portfolio.risk_reporting.phase157_models import (
    SandboxExposureGovernanceRecord,
    create_sandbox_exposure_governance_record_id
)
from usa_signal_bot.core.enums import ExposureGovernanceKind

def build_sandbox_exposure_governance_records(objective_comparison_payload: Dict[str, Any]) -> List[SandboxExposureGovernanceRecord]:
    return []

def validate_sandbox_exposure_governance_records(items: List[SandboxExposureGovernanceRecord]) -> List[str]:
    errs = []
    for item in items:
        if item.actual_target_weight is not None: errs.append("actual_target_weight must be None")
        if item.actual_portfolio_weight is not None: errs.append("actual_portfolio_weight must be None")
        if item.actual_allocation is not None: errs.append("actual_allocation must be None")
        if item.actual_position_size is not None: errs.append("actual_position_size must be None")
        if item.order_size is not None: errs.append("order_size must be None")
        if item.capital_allocation is not None: errs.append("capital_allocation must be None")
        if not item.research_exposure_only: errs.append("research_exposure_only must be True")
    return errs

def sandbox_exposure_governance_summary(items: List[SandboxExposureGovernanceRecord]) -> Dict[str, Any]:
    return {"count": len(items)}

def sandbox_exposure_governance_to_text(items: List[SandboxExposureGovernanceRecord], limit: int = 300) -> str:
    return f"Governance Exposures: {len(items)}"
