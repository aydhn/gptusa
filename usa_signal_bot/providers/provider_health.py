from typing import Any

from usa_signal_bot.providers.provider_interface import BaseDataProvider
from usa_signal_bot.providers.provider_models import ProviderHealthResult

class ProviderHealthChecker:
    def __init__(self, providers: list[BaseDataProvider]):
        self.providers = providers

    def check_all(self) -> list[ProviderHealthResult]:
        results = []
        for p in self.providers:
            results.append(self.check_provider(p))
        return results

    def check_provider(self, provider: BaseDataProvider) -> ProviderHealthResult:
        try:
            return provider.health_check()
        except Exception as e:
            from datetime import datetime, timezone
            from usa_signal_bot.providers.provider_models import create_provider_health_id
            from usa_signal_bot.core.enums import ProviderQualityStatus
            return ProviderHealthResult(
                health_id=create_provider_health_id(),
                provider_name=provider.name(),
                checked_at_utc=datetime.now(timezone.utc).isoformat(),
                status=ProviderQualityStatus.FAILED,
                reachable=False,
                capability_status={},
                errors=[f"Health check failed with exception: {str(e)}"]
            )

    def summarize_health(self, results: list[ProviderHealthResult]) -> dict[str, Any]:
        from usa_signal_bot.core.enums import ProviderQualityStatus
        summary = {
            "total_providers": len(results),
            "reachable": sum(1 for r in results if r.reachable),
            "unreachable": sum(1 for r in results if not r.reachable),
            "healthy": sum(1 for r in results if r.status in [ProviderQualityStatus.EXCELLENT, ProviderQualityStatus.GOOD, ProviderQualityStatus.ACCEPTABLE]),
            "degraded": sum(1 for r in results if r.status == ProviderQualityStatus.DEGRADED),
            "failed": sum(1 for r in results if r.status in [ProviderQualityStatus.POOR, ProviderQualityStatus.FAILED]),
        }
        return summary

def provider_health_result_to_text(result: ProviderHealthResult) -> str:
    lines = [
        f"--- Health Result: {result.provider_name.value} ---",
        f"Status: {result.status.value}",
        f"Reachable: {result.reachable}"
    ]
    if result.latency_ms is not None:
        lines.append(f"Latency: {result.latency_ms:.2f}ms")
    if result.warnings:
        lines.append(f"Warnings: {len(result.warnings)}")
        for w in result.warnings:
            lines.append(f"  - {w}")
    if result.errors:
        lines.append(f"Errors: {len(result.errors)}")
        for e in result.errors:
            lines.append(f"  - {e}")
    return "\n".join(lines)

def provider_health_summary_to_text(summary: dict[str, Any]) -> str:
    lines = [
        "--- Provider Health Summary ---",
        f"Total Providers: {summary['total_providers']}",
        f"Reachable: {summary['reachable']}",
        f"Unreachable: {summary['unreachable']}",
        f"Healthy: {summary['healthy']}",
        f"Degraded: {summary['degraded']}",
        f"Failed: {summary['failed']}"
    ]
    return "\n".join(lines)
