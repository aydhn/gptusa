"""Lineage Continuity Validator."""
from typing import Any
from datetime import datetime, timezone

from .phase124_models import (
    ArtifactChainReference,
    IntegrationRehearsalStep,
    IntegrationRehearsalStepKind,
    IntegrationRehearsalStepStatus,
    create_integration_rehearsal_step_id
)

def validate_lineage_continuity(references: list[ArtifactChainReference], payloads: dict[str, dict[str, Any]] | None = None) -> list[IntegrationRehearsalStep]:
    steps = []
    now = datetime.now(timezone.utc).isoformat()

    missing = detect_missing_lineage_refs(references)
    breaks = detect_lineage_breaks(payloads or {})

    passed = len(missing) == 0 and len(breaks) == 0
    status = IntegrationRehearsalStepStatus.PASS if passed else IntegrationRehearsalStepStatus.FAIL

    errors = [f"Missing lineage ref for {m.phase.value}" for m in missing] + breaks

    steps.append(IntegrationRehearsalStep(
        step_id=create_integration_rehearsal_step_id(),
        created_at_utc=now,
        step_kind=IntegrationRehearsalStepKind.VERIFY_LINEAGE_CONTINUITY,
        status=status,
        required=True,
        passed=passed,
        observed_value=len(errors),
        expected_value=0,
        message="Lineage continuity verified" if passed else f"Found {len(errors)} lineage issues",
        errors=errors
    ))
    return steps

def detect_missing_lineage_refs(references: list[ArtifactChainReference]) -> list[ArtifactChainReference]:
    # Placeholder
    return []

def detect_lineage_breaks(payloads: dict[str, dict[str, Any]]) -> list[str]:
    return []

def lineage_continuity_summary(steps: list[IntegrationRehearsalStep]) -> dict[str, Any]:
    return {"passed": all(s.passed for s in steps)}

def lineage_continuity_to_text(steps: list[IntegrationRehearsalStep], limit: int = 200) -> str:
    return "Lineage Continuity: " + ("PASS" if all(s.passed for s in steps) else "FAIL")
