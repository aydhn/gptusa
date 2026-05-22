from usa_signal_bot.paper_firewall_audit.firewall_replay_engine import PaperFirewallReplayEngine
from usa_signal_bot.paper_firewall_audit.firewall_replay_plan import build_default_firewall_replay_plan

def test_replay_engine():
    engine = PaperFirewallReplayEngine()
    plan = build_default_firewall_replay_plan()
    events = [{"is_dangerous": True, "blocked": True}]
    result = engine.replay(plan, events)
    assert result.passed is True
