import json
from pathlib import Path
from typing import Any
from usa_signal_bot.backtesting.basket_models import BasketReplayData, BasketReplayItem, BasketReplayRequest
from usa_signal_bot.core.enums import SignalAction, BasketReplaySource
from usa_signal_bot.core.exceptions import BasketReplayError

def load_basket_replay_data(data_root: Path, request: BasketReplayRequest) -> BasketReplayData:
    return BasketReplayData(request=request, items=[], symbols=[], timeframe=request.timeframe, warnings=[], errors=[])

def basket_replay_data_to_text(data: BasketReplayData, limit: int = 30) -> str:
    return "basket replay data"
