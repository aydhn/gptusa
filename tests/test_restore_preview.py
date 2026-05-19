from usa_signal_bot.release_packaging.restore_preview import restore_preview_to_text

def test_restore_preview():
    assert "Preview for" in restore_preview_to_text({"bundle_id": "1", "restore_allowed": True})
