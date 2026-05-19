from typing import Any, List, Optional, Dict

def normalize_bundle_version(version: Optional[str]) -> str:
    if not version:
        return "0.1.0"
    return version.strip()

def generate_bundle_version(base_version: str = "0.1.0", build_number: Optional[int] = None, suffix: Optional[str] = None) -> str:
    ver = normalize_bundle_version(base_version)
    if build_number is not None:
        ver = f"{ver}+{build_number}"
    if suffix:
        ver = f"{ver}-{suffix}"
    return ver

def next_patch_version(version: str) -> str:
    parts = version.split(".")
    if len(parts) >= 3:
        try:
            patch = int(parts[2].split("+")[0].split("-")[0])
            parts[2] = str(patch + 1)
            return ".".join(parts)
        except ValueError:
            pass
    return version

def version_from_candidate_metadata(candidate_payload: Optional[Dict[str, Any]] = None) -> str:
    return "0.1.0"

def validate_bundle_version(version: str) -> List[str]:
    warnings = []
    if not version:
        warnings.append("Version is empty.")
    return warnings

def compare_bundle_versions(version_a: str, version_b: str) -> int:
    # simple comparison
    return (version_a > version_b) - (version_a < version_b)

def bundle_versioning_to_text(version: str) -> str:
    return f"Bundle Version: {version}"
