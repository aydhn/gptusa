from typing import Any, Dict, List
from usa_signal_bot.regime_classification.freeze_preparation.phase134_models import (
    ResearchFreezePackage,
    ResearchFreezeArtifactReference
)
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_package_builder import validate_required_artifact_coverage
from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_hashing import (
    compute_research_freeze_package_hash,
    compute_research_freeze_manifest_hash
)

def validate_research_freeze_artifact_references(references: List[ResearchFreezeArtifactReference]) -> List[str]:
    return validate_required_artifact_coverage(references)

def validate_research_freeze_package_hashes(package: ResearchFreezePackage) -> List[str]:
    errors = []
    if package.package_hash != compute_research_freeze_package_hash(package):
        errors.append("Invalid package_hash")
    if package.manifest_hash != compute_research_freeze_manifest_hash(package):
        errors.append("Invalid manifest_hash")
    return errors

def validate_research_freeze_package_safety_flags(package: ResearchFreezePackage) -> List[str]:
    from usa_signal_bot.regime_classification.freeze_preparation.research_freeze_safety_validator import validate_freeze_package_safety
    return validate_freeze_package_safety(package)

def validate_research_freeze_package(package: ResearchFreezePackage) -> List[str]:
    errors = []
    errors.extend(validate_research_freeze_artifact_references(package.artifact_references))
    errors.extend(validate_research_freeze_package_hashes(package))
    errors.extend(validate_research_freeze_package_safety_flags(package))
    if not package.package_valid:
        errors.append("package_valid is False")
    return errors

def research_freeze_package_validator_summary(errors: List[str]) -> Dict[str, Any]:
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

def research_freeze_package_validator_to_text(errors: List[str]) -> str:
    if not errors:
        return "Package Validation Passed."
    return f"Package Validation Failed with {len(errors)} errors:\n" + "\n".join(f"- {e}" for e in errors)
