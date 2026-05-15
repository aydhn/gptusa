def update_exceptions():
    with open('usa_signal_bot/core/exceptions.py', 'r') as f:
        content = f.read()

    new_exceptions = """
class RegimeAwareCostError(USASignalBotError):
    pass

class VolatilityRegimeCostError(RegimeAwareCostError):
    pass

class LiquidityRegimeCostError(RegimeAwareCostError):
    pass

class SpreadRegimeCostError(RegimeAwareCostError):
    pass

class SessionRegimeCostError(RegimeAwareCostError):
    pass

class LifecycleRegimeCostError(RegimeAwareCostError):
    pass

class CombinedCostRegimeError(RegimeAwareCostError):
    pass

class CostCurveSelectionError(RegimeAwareCostError):
    pass

class AdaptiveExecutionRealismError(RegimeAwareCostError):
    pass

class RegimeCostBreakdownError(RegimeAwareCostError):
    pass

class RegimeCostStorageError(RegimeAwareCostError):
    pass

class RegimeCostValidationError(RegimeAwareCostError):
    pass

class RegimeCostReportingError(RegimeAwareCostError):
    pass
"""
    if "RegimeAwareCostError" not in content:
        content += new_exceptions
        with open('usa_signal_bot/core/exceptions.py', 'w') as f:
            f.write(content)

update_exceptions()
