import re

with open("usa_signal_bot/core/exceptions.py", "r") as f:
    content = f.read()

new_exceptions = """
class StrategyAdaptationError(USASignalBotError):
    pass

class StrategyRegimeProfileError(StrategyAdaptationError):
    pass

class StrategyCompatibilityError(StrategyAdaptationError):
    pass

class StrategyGatingError(StrategyAdaptationError):
    pass

class StrategyConflictResolutionError(StrategyAdaptationError):
    pass

class StrategyEnsembleError(StrategyAdaptationError):
    pass

class AdaptiveStrategyWeightError(StrategyAdaptationError):
    pass

class StrategyAdaptationStorageError(StrategyAdaptationError):
    pass

class StrategyAdaptationValidationError(StrategyAdaptationError):
    pass

class StrategyAdaptationReportingError(StrategyAdaptationError):
    pass
"""

if "class StrategyAdaptationError" not in content:
    content += "\n" + new_exceptions

with open("usa_signal_bot/core/exceptions.py", "w") as f:
    f.write(content)
