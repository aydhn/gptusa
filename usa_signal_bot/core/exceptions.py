class UsaSignalBotError(Exception):
    pass

class RegimeMapError(UsaSignalBotError):
    pass

class TimeframeResamplerError(RegimeMapError):
    pass

class TimeframeRegimeConfirmationError(RegimeMapError):
    pass

class TrendConfirmationError(RegimeMapError):
    pass

class VolatilityConfirmationError(RegimeMapError):
    pass

class MomentumConfirmationError(RegimeMapError):
    pass

class LiquidityConfirmationError(RegimeMapError):
    pass

class BreadthProxyError(RegimeMapError):
    pass

class DispersionProxyError(RegimeMapError):
    pass

class CrossSectionalRegimeMapError(RegimeMapError):
    pass

class SymbolRegimeAlignmentError(RegimeMapError):
    pass

class RegimeTransitionDetectorError(RegimeMapError):
    pass

class RegimeTransitionRiskError(RegimeMapError):
    pass

class RegimeMapStorageError(RegimeMapError):
    pass

class RegimeMapValidationError(RegimeMapError):
    pass

class RegimeMapReportingError(RegimeMapError):
    pass
