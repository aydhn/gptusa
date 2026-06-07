from usa_signal_bot.backtesting.closure.phase152_models import *

def build_safe_phase152_gate() -> Phase153ReadinessGate:
    gate = Phase153ReadinessGate(ready_for_phase153=True)
    gate.status = Phase153ReadinessStatus.PASSED
    return gate
