from usa_signal_bot.release_packaging.bundle_readme import generate_bundle_limitations_section

def test_readme():
    lims = generate_bundle_limitations_section()
    assert "No broker/live/demo order execution" in lims
