from usa_signal_bot.release_packaging.bundle_diff import bundle_diff_summary

def test_diff():
    assert bundle_diff_summary({"test": 1})["test"] == 1
