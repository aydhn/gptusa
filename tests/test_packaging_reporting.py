from usa_signal_bot.release_packaging.packaging_reporting import release_packaging_limitations_text

def test_reporting():
    assert "local research package only" in release_packaging_limitations_text()
