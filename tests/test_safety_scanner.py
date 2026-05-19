from usa_signal_bot.release_packaging.safety_scanner import scan_text_for_secret_like_patterns
from usa_signal_bot.core.enums import BundleSafetyFlag

def test_safety_scanner():
    flags = scan_text_for_secret_like_patterns("this is an api_key")
    assert BundleSafetyFlag.SECRET_LEAK_RISK in flags
