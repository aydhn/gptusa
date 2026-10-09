"""Common helpers shared by paper_* packages (plain IO, validation dataclasses)."""
from usa_signal_bot.paper_common.io import (
    append_jsonl,
    count_files,
    ensure_dir,
    latest_by_mtime,
    list_files,
    read_json,
    read_jsonl,
    write_json,
    write_jsonl,
)
from usa_signal_bot.paper_common.validation_types import ValidationIssue, ValidationReport

__all__ = [
    "append_jsonl", "count_files", "ensure_dir", "latest_by_mtime", "list_files",
    "read_json", "read_jsonl", "write_json", "write_jsonl",
    "ValidationIssue", "ValidationReport",
]
