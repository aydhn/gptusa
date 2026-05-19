from usa_signal_bot.release_packaging.checksum import stable_payload_hash, verify_payload_hash

def test_checksum():
    p1 = {"a": 1, "b": 2}
    p2 = {"b": 2, "a": 1}
    assert stable_payload_hash(p1) == stable_payload_hash(p2)
    assert verify_payload_hash(p1, stable_payload_hash(p1)) is True
