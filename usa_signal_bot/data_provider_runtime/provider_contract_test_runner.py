from typing import Any, List
from datetime import datetime, timezone
import inspect

from usa_signal_bot.data_provider_runtime.phase107_models import (
    ProviderContractTestItem,
    ProviderContractTestReport,
    create_provider_contract_test_id,
    create_provider_contract_test_report_id,
    ProviderRuntimeAdapterSpec
)
from usa_signal_bot.core.enums import ProviderContractTestStatus, ProviderRuntimeStatus, ProviderRuntimeRiskFlag


class ProviderContractTestRunner:
    def __init__(self, specs: List[ProviderRuntimeAdapterSpec]):
        self.specs = specs

    def run_all_contract_tests(self) -> ProviderContractTestReport:
        report = ProviderContractTestReport(
            report_id=create_provider_contract_test_report_id(),
            created_at_utc=datetime.now(timezone.utc).isoformat(),
            status=ProviderRuntimeStatus.DRAFT
        )

        all_items = []
        for spec in self.specs:
            if spec.supports_contract_tests:
                adapter = self._instantiate_adapter(spec)
                if adapter:
                    items = self.run_adapter_contract_tests(adapter, spec)
                    all_items.extend(items)
                else:
                    item = ProviderContractTestItem(
                        test_id=create_provider_contract_test_id(),
                        provider_name=spec.provider_name,
                        adapter_class=spec.adapter_class,
                        test_name="instantiation",
                        status=ProviderContractTestStatus.FAIL,
                        message="Failed to instantiate adapter"
                    )
                    all_items.append(item)

        return self.summarize(all_items, report)

    def _instantiate_adapter(self, spec: ProviderRuntimeAdapterSpec) -> Any:
        import importlib
        try:
            mod = importlib.import_module(spec.adapter_module)
            cls = getattr(mod, spec.adapter_class)
            return cls()
        except Exception as e:
            return None

    def run_adapter_contract_tests(self, adapter: Any, spec: ProviderRuntimeAdapterSpec) -> List[ProviderContractTestItem]:
        items = []
        items.append(self.test_adapter_spec(adapter, spec))
        items.append(self.test_no_forbidden_methods(adapter, spec))
        items.append(self.test_metadata_only_execution(adapter, spec))
        items.append(self.test_no_network_default(adapter, spec))
        items.append(self.test_schema_normalization(adapter, spec))
        return items

    def test_adapter_spec(self, adapter: Any, spec: ProviderRuntimeAdapterSpec) -> ProviderContractTestItem:
        item = ProviderContractTestItem(
            provider_name=spec.provider_name,
            adapter_class=spec.adapter_class,
            test_name="adapter_spec",
        )
        try:
            a_spec = adapter.adapter_spec()
            if a_spec:
                item.status = ProviderContractTestStatus.PASS
                item.message = "adapter_spec method returned valid spec"
            else:
                item.status = ProviderContractTestStatus.FAIL
                item.message = "adapter_spec method returned None"
        except Exception as e:
            item.status = ProviderContractTestStatus.FAIL
            item.message = f"Exception: {str(e)}"
        return item

    def test_no_forbidden_methods(self, adapter: Any, spec: ProviderRuntimeAdapterSpec) -> ProviderContractTestItem:
        item = ProviderContractTestItem(
            provider_name=spec.provider_name,
            adapter_class=spec.adapter_class,
            test_name="no_forbidden_methods",
        )
        forbidden = ["order", "broker", "trade", "scrape", "html", "selenium", "playwright", "live", "paper_order", "send_order", "place_order"]
        methods = [m[0] for m in inspect.getmembers(adapter, predicate=inspect.ismethod)]

        found = []
        for m in methods:
            for f in forbidden:
                if f in m.lower():
                    found.append(m)

        if found:
            item.status = ProviderContractTestStatus.FAIL
            item.message = f"Found forbidden methods: {', '.join(found)}"
            item.risk_flags.append(ProviderRuntimeRiskFlag.BROKER_RISK)
        else:
            item.status = ProviderContractTestStatus.PASS
            item.message = "No forbidden methods found"

        return item

    def test_metadata_only_execution(self, adapter: Any, spec: ProviderRuntimeAdapterSpec) -> ProviderContractTestItem:
        item = ProviderContractTestItem(
            provider_name=spec.provider_name,
            adapter_class=spec.adapter_class,
            test_name="metadata_only_execution",
        )
        try:
            if hasattr(adapter, "build_daily_ohlcv_plan") and hasattr(adapter, "execute_metadata_only"):
                plan = adapter.build_daily_ohlcv_plan("AAPL")
                res = adapter.execute_metadata_only(plan)
                if isinstance(res, dict) and "metadata_only" in res:
                    item.status = ProviderContractTestStatus.PASS
                    item.message = "execute_metadata_only returned valid dict"
                else:
                    item.status = ProviderContractTestStatus.FAIL
                    item.message = "execute_metadata_only did not return expected format"
            else:
                item.status = ProviderContractTestStatus.SKIPPED
                item.message = "Missing metadata_only_execution methods"
        except Exception as e:
            item.status = ProviderContractTestStatus.FAIL
            item.message = f"Exception: {str(e)}"
        return item

    def test_no_network_default(self, adapter: Any, spec: ProviderRuntimeAdapterSpec) -> ProviderContractTestItem:
        item = ProviderContractTestItem(
            provider_name=spec.provider_name,
            adapter_class=spec.adapter_class,
            test_name="no_network_default",
        )
        try:
            if hasattr(adapter, "fetch_daily_ohlcv_guarded"):
                res = adapter.fetch_daily_ohlcv_guarded("AAPL", allow_network=False)
                if not res.get("network_used", True):
                    item.status = ProviderContractTestStatus.PASS
                    item.message = "network_used=False when allow_network=False"
                else:
                    item.status = ProviderContractTestStatus.FAIL
                    item.message = "network_used=True despite allow_network=False"
            else:
                item.status = ProviderContractTestStatus.SKIPPED
                item.message = "No fetch_daily_ohlcv_guarded method found"
        except Exception as e:
            item.status = ProviderContractTestStatus.FAIL
            item.message = f"Exception: {str(e)}"
        return item

    def test_schema_normalization(self, adapter: Any, spec: ProviderRuntimeAdapterSpec) -> ProviderContractTestItem:
        item = ProviderContractTestItem(
            provider_name=spec.provider_name,
            adapter_class=spec.adapter_class,
            test_name="schema_normalization",
        )
        try:
            if hasattr(adapter, "normalize_sample"):
                res = adapter.normalize_sample()
                if "symbol" in res and "close" in res:
                    item.status = ProviderContractTestStatus.PASS
                    item.message = "normalize_sample returned canonical keys"
                else:
                    item.status = ProviderContractTestStatus.FAIL
                    item.message = "normalize_sample missing required canonical keys"
            else:
                item.status = ProviderContractTestStatus.SKIPPED
                item.message = "No normalize_sample method found"
        except Exception as e:
            item.status = ProviderContractTestStatus.FAIL
            item.message = f"Exception: {str(e)}"
        return item

    def summarize(self, items: List[ProviderContractTestItem], report: ProviderContractTestReport) -> ProviderContractTestReport:
        report.items = items
        report.total_tests = len(items)
        report.passed_tests = sum(1 for i in items if i.status == ProviderContractTestStatus.PASS)
        report.warning_tests = sum(1 for i in items if i.status == ProviderContractTestStatus.WARNING)
        report.failed_tests = sum(1 for i in items if i.status == ProviderContractTestStatus.FAIL)
        report.blocked_tests = sum(1 for i in items if i.status == ProviderContractTestStatus.BLOCKED)
        report.skipped_tests = sum(1 for i in items if i.status == ProviderContractTestStatus.SKIPPED)

        report.contract_tests_passed = report.failed_tests == 0 and report.blocked_tests == 0

        if report.contract_tests_passed:
            report.status = ProviderRuntimeStatus.VALIDATED
        else:
            report.status = ProviderRuntimeStatus.FAILED

        return report
