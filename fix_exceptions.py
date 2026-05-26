with open('usa_signal_bot/core/exceptions.py', 'r') as f:
    content = f.read()

exceptions = """
class FeatureFoundationError(Exception):
    pass

class FeatureFactorKickoffIngestionError(FeatureFoundationError):
    pass

class IndicatorRegistryError(FeatureFoundationError):
    pass

class FeatureRegistryError(FeatureFoundationError):
    pass

class FactorRegistryError(FeatureFoundationError):
    pass

class FeatureInputContractError(FeatureFoundationError):
    pass

class FeatureSchemaError(FeatureFoundationError):
    pass

class FeatureComputationPlannerError(FeatureFoundationError):
    pass

class FeatureTransformPipelineError(FeatureFoundationError):
    pass

class FeatureOutputContractError(FeatureFoundationError):
    pass

class FeatureLineageError(FeatureFoundationError):
    pass

class FeatureSafetyValidationError(FeatureFoundationError):
    pass

class FeatureFoundationStoreError(FeatureFoundationError):
    pass

class FeatureFoundationValidationError(FeatureFoundationError):
    pass

class FeatureFoundationReportingError(FeatureFoundationError):
    pass
"""

with open('usa_signal_bot/core/exceptions.py', 'w') as f:
    f.write(content + exceptions)
