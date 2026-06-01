import pandas as pd
from usa_signal_bot.ml_research.ensemble_evaluation.ensemble_input_resolver import build_ensemble_prototype_input_references, validate_prediction_frame_for_ensemble

def test_build_ensemble_prototype_input_references():
    blend_plans = [{"candidate_group_id": "g1", "blend_plan_id": "bp1"}]
    refs = build_ensemble_prototype_input_references([], [], [], blend_plans, [])
    assert len(refs) == 1
    assert refs[0].research_data_only is True
    assert refs[0].contains_forbidden_outputs is False

def test_validate_prediction_frame_for_ensemble():
    df = pd.DataFrame({"symbol": ["AAPL"], "timestamp": ["2023-01-01"], "split_name": ["test"], "buy_signal": [1]})
    errors = validate_prediction_frame_for_ensemble(df)
    assert len(errors) == 1
    assert "Forbidden column detected" in errors[0]
