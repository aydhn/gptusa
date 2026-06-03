from usa_signal_bot.backtesting.benchmark_comparison.phase149_models import *
import re
def benchmark_text_has_trade_or_execution_language(text: str) -> bool:
    return bool(re.search(r'\bdefinitely buy\b', text.lower()))
