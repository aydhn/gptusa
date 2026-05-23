
from usa_signal_bot.paper_no_write_transition.bridge_route_guard import validate_all_bridge_routes_no_write
def test_route_guard():
    assert isinstance(validate_all_bridge_routes_no_write([]), list)
