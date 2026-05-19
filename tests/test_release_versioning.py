from usa_signal_bot.release_packaging.versioning import generate_bundle_version

def test_versioning():
    ver = generate_bundle_version("0.1.0", 1, "local")
    assert ver == "0.1.0+1-local"
