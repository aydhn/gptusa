from typing import Any
from pathlib import Path
import re
from usa_signal_bot.core.exceptions import CachePathResolverError

def sanitize_provider_cache_part(value: str) -> str:
    # Remove any non-alphanumeric/underscore/dash characters
    s = re.sub(r'[^a-zA-Z0-9_-]', '', value)
    if not s:
        raise CachePathResolverError(f"Invalid cache path part after sanitization: '{value}'")
    return s

def default_provider_cache_root(data_root: Path) -> Path:
    return data_root / "market_data" / "cache"

def provider_cache_namespace_dir(cache_root: Path, namespace: str) -> Path:
    ns = sanitize_provider_cache_part(namespace)
    return cache_root / ns

def provider_symbol_cache_dir(cache_root: Path, provider_name: str, symbol: str) -> Path:
    p_name = sanitize_provider_cache_part(provider_name)
    sym = sanitize_provider_cache_part(symbol)
    return cache_root / p_name / sym

def resolve_provider_cache_path(cache_root: Path, provider_name: str, symbol: str, cache_key: str, extension: str = ".csv") -> Path:
    p_name = sanitize_provider_cache_part(provider_name)
    sym = sanitize_provider_cache_part(symbol)
    ck = sanitize_provider_cache_part(cache_key)

    # Simple validation against path traversal
    if ".." in extension or "/" in extension or "\\" in extension:
         raise CachePathResolverError("Invalid extension")

    return cache_root / p_name / sym / f"{ck}{extension}"

def validate_cache_path_safe(path: Path, root: Path) -> list[str]:
    try:
        resolved_path = path.resolve()
        resolved_root = root.resolve()
        if not str(resolved_path).startswith(str(resolved_root)):
            return ["Path traversal detected: Path is outside the cache root."]
        return []
    except Exception as e:
        return [f"Path validation error: {str(e)}"]

def cache_path_resolver_summary(path: Path, root: Path) -> dict[str, Any]:
    safe_errors = validate_cache_path_safe(path, root)
    return {
        "path": str(path),
        "root": str(root),
        "is_safe": len(safe_errors) == 0,
        "errors": safe_errors
    }
