try:
    import pandas as pd
except ImportError:
    pass
def add_candidate_distance_context_columns(df, candidates: list):
    for c in candidates: df[f"{c.candidate_name}_distance"] = 0.0
    return df
