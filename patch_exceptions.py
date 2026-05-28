with open("usa_signal_bot/core/exceptions.py", "a") as f:
    f.write("""
class RegimeFeatureEngineeringError(USASignalBotError):
    pass

class RegimeFoundationIngestionError(RegimeFeatureEngineeringError):
    pass

class MarketStateInputLoaderError(RegimeFeatureEngineeringError):
    pass

class MarketStateMetricSpecError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureSpecError(RegimeFeatureEngineeringError):
    pass

class MarketStateMetricsEngineError(RegimeFeatureEngineeringError):
    pass

class RollingMarketStateMetricsError(RegimeFeatureEngineeringError):
    pass

class CrossSectionalMarketStateMetricsError(RegimeFeatureEngineeringError):
    pass

class FactorContextRegimeMapperError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureTableBuilderError(RegimeFeatureEngineeringError):
    pass

class RegimeCandidateDefinitionError(RegimeFeatureEngineeringError):
    pass

class UnsupervisedCandidatePreparationError(RegimeFeatureEngineeringError):
    pass

class CandidateDistanceContextError(RegimeFeatureEngineeringError):
    pass

class CandidateReadinessGateError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureSchemaValidationError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureOutputSafetyValidationError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureEngineeringStoreError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureEngineeringValidationError(RegimeFeatureEngineeringError):
    pass

class RegimeFeatureEngineeringReportingError(RegimeFeatureEngineeringError):
    pass
""")
