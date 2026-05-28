from usa_signal_bot.regime_classification.feature_engineering.phase127_models import RegimeFeatureEngineeringContext

class MockRep:
    def __init__(self, v): self.valid = v
    errors = []

def validate_regime_feature_engineering_context_report(ctx):
    rep = MockRep(not ctx.activation_allowed)
    if not rep.valid:
        rep.errors.append("Invalid")
    return rep
