import json
def write_regime_feature_engineering_full_review_json(p, i):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w") as f: json.dump({"review_id": i.review_id}, f)
def read_regime_feature_engineering_full_review_json(p):
    with open(p, "r") as f: return json.load(f)
