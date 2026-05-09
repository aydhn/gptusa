import fnmatch
from pathlib import Path

def default_protected_path_patterns() -> list[str]:
    return [
        ".env",
        "*.key",
        "*token*",
        "*secret*",
        "credentials*",
        "config/default.yaml",
        "config/local.example.yaml",
        "config/profiles/*",
        "requirements.txt",
        "usa_signal_bot/**",
        "tests/**",
        "docs/**",
        "README*",
        "RELEASE_MANIFEST*",
        "OPERATOR_RUNBOOK*",
        "latest release bundles",
        "latest backup files",
        "golden baselines",
        "regression baselines"
    ]

def is_secret_like_path(path: Path) -> bool:
    name_lower = path.name.lower()
    return any(p in name_lower for p in ["secret", "token", "key", "credential"]) or name_lower == ".env"

def is_protected_path(path: Path, project_root: Path | None = None, data_root: Path | None = None, extra_patterns: list[str] | None = None) -> bool:
    if is_secret_like_path(path):
        return True

    path_str = str(path)

    if project_root:
        try:
            rel_path = path.relative_to(project_root)
            path_str = str(rel_path)
        except ValueError:
            pass

    patterns = default_protected_path_patterns()
    if extra_patterns:
        patterns.extend(extra_patterns)

    for pattern in patterns:
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if path_str.startswith(prefix) or path_str.startswith(prefix.replace('/', '\\')):
                return True
        elif fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(path.name, pattern):
            return True

    return False

def explain_protected_path(path: Path, project_root: Path | None = None, data_root: Path | None = None) -> str | None:
    if is_secret_like_path(path):
        return "Matches secret-like pattern"
    if is_protected_path(path, project_root, data_root):
         return "Matches protected path pattern"
    return None

def filter_unprotected_paths(paths: list[Path], project_root: Path | None = None, data_root: Path | None = None) -> list[Path]:
    return [p for p in paths if not is_protected_path(p, project_root, data_root)]

def protected_paths_to_text(patterns: list[str]) -> str:
    return "\n".join(f"- {p}" for p in patterns)
