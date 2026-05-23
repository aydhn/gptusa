from usa_signal_bot.paper_safe_dossier.runtime_route_map import build_runtime_route_map_items
from usa_signal_bot.core.enums import RuntimeRoutePermission

def test_runtime_route_map():
    items = build_runtime_route_map_items({})
    assert len(items) > 0

    write_route = [i for i in items if i.route_name == "paper_state_write_route"][0]
    assert write_route.permission == RuntimeRoutePermission.WRITE_DENIED
    assert write_route.write_allowed is False
    assert write_route.read_only_allowed is False

    read_route = [i for i in items if i.route_name == "read_market_data_route"][0]
    assert read_route.permission == RuntimeRoutePermission.READ_ONLY_ALLOWED
    assert read_route.read_only_allowed is True
