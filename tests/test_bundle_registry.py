from usa_signal_bot.release_packaging.bundle_registry import register_bundle

def test_registry():
    assert len(register_bundle("bundle", [])) == 1
