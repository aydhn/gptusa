import pytest
from usa_signal_bot.release_sandbox.overlay_resolver import (
    extract_candidate_overlay_from_bundle, build_in_memory_candidate_config,
    validate_overlay_does_not_patch_files, validate_overlay_has_no_broker_live_fields,
    overlay_resolver_to_text
)

def test_extract_overlay():
    payload = {"overlay": {"key1": "val1"}}
    ov = extract_candidate_overlay_from_bundle(payload)
    assert ov["key1"] == "val1"

    in_mem = build_in_memory_candidate_config(payload)
    assert in_mem["key1"] == "val1"

def test_validate_overlay_patches():
    ov = {"patch_files": True}
    warns = validate_overlay_does_not_patch_files(ov)
    assert len(warns) == 1
    assert "patch files" in warns[0]

def test_validate_overlay_broker_fields():
    ov = {"live_enabled": True, "order_routing_enabled": True}
    warns = validate_overlay_has_no_broker_live_fields(ov)
    assert len(warns) == 2

def test_overlay_resolver_to_text():
    txt = overlay_resolver_to_text({"key1": "val1", "key2": "val2"})
    assert "2 keys configured" in txt
