from pathlib import Path
from usa_signal_bot.release.versioning import build_release_version
from usa_signal_bot.release.changelog import (
    generate_changelog_entry_for_release, changelog_entry_to_dict, changelog_entries_to_markdown, write_changelog_markdown
)

def test_generate_changelog_entry_for_release(tmp_path):
    v = build_release_version("1.0.0")

    sum_path = tmp_path / "PHASE_1_SUMMARY.md"
    sum_path.write_text("- Added feature A\n- Fixed bug B", encoding="utf-8")

    entry = generate_changelog_entry_for_release(v, [sum_path])
    assert "Added feature A" in entry.changes[0] or "Added feature A" in entry.changes[1]

    d = changelog_entry_to_dict(entry)
    assert d["version"] == "1.0.0"

    md = changelog_entries_to_markdown([entry])
    assert "Changelog" in md

    out = tmp_path / "CHANGELOG.md"
    write_changelog_markdown(out, [entry])
    assert out.exists()
