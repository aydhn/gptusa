import re

with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

new_exceptions = """
class RegimeLabelingError(USAError):
    pass

class RegimeFeatureEngineeringIngestionError(RegimeLabelingError):
    pass

class RegimeLabelInputLoaderError(RegimeLabelingError):
    pass

class RegimeLabelingSpecError(RegimeLabelingError):
    pass

class HeuristicLabelingRuleError(RegimeLabelingError):
    pass

class CandidateScoreResolverError(RegimeLabelingError):
    pass

class RollingRegimeWindowError(RegimeLabelingError):
    pass

class RegimeLabelSequenceError(RegimeLabelingError):
    pass

class LabelConflictDetectorError(RegimeLabelingError):
    pass

class LabelConfidenceProxyError(RegimeLabelingError):
    pass

class CandidateValidationRunnerError(RegimeLabelingError):
    pass

class LabelStabilityProfilerError(RegimeLabelingError):
    pass

class RegimeLabelingReadinessGateError(RegimeLabelingError):
    pass

class RegimeLabelSchemaValidationError(RegimeLabelingError):
    pass

class RegimeLabelSafetyValidationError(RegimeLabelingError):
    pass

class RegimeLabelingStoreError(RegimeLabelingError):
    pass

class RegimeLabelingValidationError(RegimeLabelingError):
    pass

class RegimeLabelingReportingError(RegimeLabelingError):
    pass
"""

if "class RegimeLabelingError" not in content:
    content += "\n" + new_exceptions

with open("usa_signal_bot/core/exceptions.py", "w") as f:
    f.write(content)
