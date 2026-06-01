with open('usa_signal_bot/core/exceptions.py', 'r') as f:
    content = f.read()

new_exceptions = """

class CalibrationDiagnosticsError(UsaSignalBotError): pass
class ModelComparisonIngestionError(UsaSignalBotError): pass
class ModelComparisonArtifactLoaderError(UsaSignalBotError): pass
class CalibrationInputResolverError(UsaSignalBotError): pass
class ReliabilityBinningEngineError(UsaSignalBotError): pass
class CalibrationMetricCalculatorError(UsaSignalBotError): pass
class BrierDecompositionError(UsaSignalBotError): pass
class ScoreDistributionDiagnosticsError(UsaSignalBotError): pass
class ClassBalanceDiagnosticsError(UsaSignalBotError): pass
class PostTrainingValidationError(UsaSignalBotError): pass
class CalibrationGovernanceError(UsaSignalBotError): pass
class ModelCardCalibrationUpdaterError(UsaSignalBotError): pass
class CalibrationReadinessGateError(UsaSignalBotError): pass
class CalibrationDiagnosticsSchemaValidationError(UsaSignalBotError): pass
class CalibrationDiagnosticsSafetyValidationError(UsaSignalBotError): pass
class CalibrationDiagnosticsStoreError(UsaSignalBotError): pass
class CalibrationDiagnosticsValidationError(UsaSignalBotError): pass
class CalibrationDiagnosticsReportingError(UsaSignalBotError): pass
"""

if "CalibrationDiagnosticsError" not in content:
    content += new_exceptions

with open('usa_signal_bot/core/exceptions.py', 'w') as f:
    f.write(content)
