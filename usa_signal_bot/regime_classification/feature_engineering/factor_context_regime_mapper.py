try:
    import pandas as pd
except ImportError:
    pass
from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureSpec

def map_factor_context_to_regime_features(df, specs: list[RegimeFeatureSpec] | None = None):
    if specs is None:
        from usa_signal_bot.regime_classification.feature_engineering.regime_feature_specs import build_default_regime_feature_specs
        specs = build_default_regime_feature_specs()
    for s in specs:
        df[s.output_column] = pd.Series(0.0, index=df.index)
        if s.source_metric_names and s.source_metric_names[0] in df.columns:
            df[s.output_column] = df[s.source_metric_names[0]].clip(-1, 1)
    return df
