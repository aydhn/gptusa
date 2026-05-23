
from usa_signal_bot.paper_no_write_transition.sandbox_bridge_route_map import default_sandbox_bridge_routes
def test_bridge_routes():
    assert len(default_sandbox_bridge_routes()) > 0
