"""Text manipulation utilities."""

def contains_sensitive_key(text: str) -> bool:
    """Checks if a string contains typical sensitive key words."""
    sensitive_keywords = ["token", "secret", "password", "api_key", "key"]
    return any(keyword in text.lower() for keyword in sensitive_keywords)

def redact_sensitive_text(text: str) -> str:
    """Redacts values in a text if it seems to contain a secret."""
    # A simple redaction logic for text format: if it contains sensitive keys, we mask it
    # For Phase 3, this is a basic implementation to handle string representations.
    if contains_sensitive_key(text):
        return "***REDACTED***"
    return text

def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncates text to a maximum length."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text

def clean_symbol_for_filename(symbol: str) -> str:
    """Cleans a symbol string to be safe for filenames."""
    # Replace characters that might be problematic in filenames
    import re
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', symbol).upper()
