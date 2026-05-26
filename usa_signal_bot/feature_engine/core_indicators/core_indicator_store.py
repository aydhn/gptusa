from pathlib import Path
from usa_signal_bot.feature_engine.core_indicators.phase117_models import CoreIndicatorFullReview
import pandas as pd
import json

def write_core_indicator_full_review_json(p: Path, rev: CoreIndicatorFullReview):
    from usa_signal_bot.feature_engine.core_indicators.phase117_models import core_indicator_full_review_to_dict
    with open(p, "w") as f: json.dump(core_indicator_full_review_to_dict(rev), f)

def read_core_indicator_full_review_json(p: Path):
    with open(p, "r") as f: return json.load(f)

def write_feature_table_csv(p: Path, df: pd.DataFrame, overwrite: bool = False):
    df.to_csv(p, index=False)
