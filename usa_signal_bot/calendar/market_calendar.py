"""Local Market Calendar Engine."""
from datetime import datetime, timedelta

from usa_signal_bot.core.enums import MarketCalendarName, MarketSessionType, MarketDayType, CalendarDataSource
from usa_signal_bot.calendar.calendar_models import MarketHoliday, MarketEarlyClose, MarketSession, TradingDayResult

class LocalMarketCalendar:
    """
    Strictly local market calendar.
    Does not use paid APIs or heavy dependencies.
    """
    def __init__(
        self,
        calendar_name: MarketCalendarName = MarketCalendarName.US_EQUITIES,
        timezone: str = "America/New_York",
        holidays: list[MarketHoliday] | None = None,
        early_closes: list[MarketEarlyClose] | None = None
    ):
        self.calendar_name = calendar_name
        self.timezone = timezone
        self._holidays = {h.date: h for h in (holidays or [])}
        self._early_closes = {c.date: c for c in (early_closes or [])}

        if self.calendar_name in [MarketCalendarName.US_EQUITIES, MarketCalendarName.US_ETF]:
            self._default_open = "09:30"
            self._default_close = "16:00"
        else:
            self._default_open = "09:00"
            self._default_close = "17:00"

    def is_weekend(self, date_str: str) -> bool:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.weekday() >= 5 # 5=Sat, 6=Sun

    def is_holiday(self, date_str: str) -> bool:
        return date_str in self._holidays

    def is_early_close(self, date_str: str) -> bool:
        return date_str in self._early_closes

    def is_trading_day(self, date_str: str) -> bool:
        if self.is_weekend(date_str):
            return False
        if self.is_holiday(date_str):
            return False
        return True

    def session_for_date(self, date_str: str) -> MarketSession:
        from usa_signal_bot.calendar.calendar_models import create_market_session_id
        session_id = create_market_session_id(self.calendar_name, date_str)

        if self.is_weekend(date_str):
            return MarketSession(
                session_id=session_id,
                calendar_name=self.calendar_name,
                date=date_str,
                session_type=MarketSessionType.WEEKEND,
                open_time_local=None,
                close_time_local=None,
                timezone=self.timezone,
                is_trading_session=False,
                is_early_close=False,
                source=CalendarDataSource.STATIC_DEFAULT
            )

        if self.is_holiday(date_str):
            h = self._holidays[date_str]
            return MarketSession(
                session_id=session_id,
                calendar_name=self.calendar_name,
                date=date_str,
                session_type=MarketSessionType.HOLIDAY,
                open_time_local=None,
                close_time_local=None,
                timezone=self.timezone,
                is_trading_session=False,
                is_early_close=False,
                source=h.source
            )

        is_early = self.is_early_close(date_str)
        close_time = self._early_closes[date_str].close_time_local if is_early else self._default_close

        return MarketSession(
            session_id=session_id,
            calendar_name=self.calendar_name,
            date=date_str,
            session_type=MarketSessionType.REGULAR,
            open_time_local=self._default_open,
            close_time_local=close_time,
            timezone=self.timezone,
            is_trading_session=True,
            is_early_close=is_early,
            source=CalendarDataSource.STATIC_DEFAULT if not is_early else self._early_closes[date_str].source
        )

    def regular_session_times(self, date_str: str) -> tuple[str, str]:
        session = self.session_for_date(date_str)
        return session.open_time_local or self._default_open, session.close_time_local or self._default_close

    def previous_trading_day(self, date_str: str, lookback_days: int = 10) -> str | None:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        for i in range(1, lookback_days + 1):
            prev_dt = dt - timedelta(days=i)
            prev_str = prev_dt.strftime("%Y-%m-%d")
            if self.is_trading_day(prev_str):
                return prev_str
        return None

    def next_trading_day(self, date_str: str, lookahead_days: int = 10) -> str | None:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        for i in range(1, lookahead_days + 1):
            next_dt = dt + timedelta(days=i)
            next_str = next_dt.strftime("%Y-%m-%d")
            if self.is_trading_day(next_str):
                return next_str
        return None

    def trading_days_between(self, start_date: str, end_date: str) -> list[str]:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        days = []
        curr = start_dt
        while curr <= end_dt:
            curr_str = curr.strftime("%Y-%m-%d")
            if self.is_trading_day(curr_str):
                days.append(curr_str)
            curr += timedelta(days=1)
        return days

    def review_range(self, start_date: str, end_date: str) -> list[TradingDayResult]:
        from usa_signal_bot.calendar.calendar_models import create_trading_day_result_id

        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        results = []
        curr = start_dt
        while curr <= end_dt:
            curr_str = curr.strftime("%Y-%m-%d")
            is_trading = self.is_trading_day(curr_str)

            day_type = MarketDayType.UNKNOWN
            if self.is_weekend(curr_str):
                day_type = MarketDayType.WEEKEND
            elif self.is_holiday(curr_str):
                day_type = MarketDayType.HOLIDAY
            elif self.is_early_close(curr_str):
                day_type = MarketDayType.EARLY_CLOSE
            elif is_trading:
                day_type = MarketDayType.TRADING_DAY
            else:
                day_type = MarketDayType.NON_TRADING_DAY

            session = self.session_for_date(curr_str)

            res = TradingDayResult(
                result_id=create_trading_day_result_id(curr_str),
                calendar_name=self.calendar_name,
                date=curr_str,
                day_type=day_type,
                is_trading_day=is_trading,
                previous_trading_day=self.previous_trading_day(curr_str) if is_trading else None,
                next_trading_day=self.next_trading_day(curr_str) if is_trading else None,
                session=session
            )
            results.append(res)
            curr += timedelta(days=1)

        return results
