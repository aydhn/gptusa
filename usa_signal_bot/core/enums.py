from enum import Enum

class AssetType(str, Enum):
    STOCK = "STOCK"
    ETF = "ETF"

class TimeFrame(str, Enum):
    ONE_MINUTE = "ONE_MINUTE"
    FIVE_MINUTES = "FIVE_MINUTES"
    FIFTEEN_MINUTES = "FIFTEEN_MINUTES"
    THIRTY_MINUTES = "THIRTY_MINUTES"
    ONE_HOUR = "ONE_HOUR"
    ONE_DAY = "ONE_DAY"
    ONE_WEEK = "ONE_WEEK"

class SignalSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    FLAT = "FLAT"

class SignalStrength(str, Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

class PositionSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    FLAT = "FLAT"

class TradeStatus(str, Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class RegimeType(str, Enum):
    UNKNOWN = "UNKNOWN"
    RISK_ON = "RISK_ON"
    RISK_OFF = "RISK_OFF"
    TRENDING_UP = "TRENDING_UP"
    TRENDING_DOWN = "TRENDING_DOWN"
    RANGE_BOUND = "RANGE_BOUND"
    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"

class DataQualityStatus(str, Enum):
    OK = "OK"
    WARNING = "WARNING"
    ERROR = "ERROR"

class BacktestStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ModelRunStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ReportFormat(str, Enum):
    TXT = "TXT"
    JSON = "JSON"
    CSV = "CSV"
    HTML_DISABLED = "HTML_DISABLED"

class DataProviderName(str, Enum):
    MOCK = "MOCK"
    YFINANCE_RESERVED = "YFINANCE_RESERVED"

class DataFrequency(str, Enum):
    DAILY = "DAILY"
    INTRADAY = "INTRADAY"
    WEEKLY = "WEEKLY"

class ProviderAvailability(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    RESERVED = "RESERVED"
    DISABLED = "DISABLED"
