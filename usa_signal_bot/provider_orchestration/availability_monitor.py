from typing import Any
from usa_signal_bot.provider_orchestration.phase110_models import DataAvailabilityItem, DataAvailabilityReport
from usa_signal_bot.provider_orchestration.cache_availability_checker import check_cache_availability_batch, check_cache_availability
from usa_signal_bot.provider_orchestration.symbol_coverage_monitor import monitor_symbol_coverage

class DataAvailabilityMonitor:
    def __init__(self, provider_quality_payload: dict[str, Any] | None = None, cache_payload: dict[str, Any] | None = None):
        self.provider_quality_payload = provider_quality_payload
        self.cache_payload = cache_payload

    def check(self, symbols: list[str], capability: str = "GET_DAILY_OHLCV") -> DataAvailabilityReport:
        items = check_cache_availability_batch(symbols, capability, self.cache_payload)
        report = monitor_symbol_coverage(symbols, capability, items)

        errors = self.validate_report_safety(report)
        if errors:
            report.errors.extend(errors)
            report.availability_ready = False

        return report

    def check_symbol(self, symbol: str, capability: str = "GET_DAILY_OHLCV") -> DataAvailabilityItem:
        return check_cache_availability(symbol, capability, None, self.cache_payload)

    def validate_report_safety(self, report: DataAvailabilityReport) -> list[str]:
        errors = []
        if report.network_used: errors.append("network_used must be False")
        if report.paid_api_used: errors.append("paid_api_used must be False")
        if report.scraping_used: errors.append("scraping_used must be False")
        if report.html_parsing_used: errors.append("html_parsing_used must be False")
        return errors

def availability_summary(report: DataAvailabilityReport) -> dict[str, Any]:
    return {
        "coverage_ratio": report.coverage_ratio,
        "missing": report.missing_count,
        "ready": report.availability_ready
    }
