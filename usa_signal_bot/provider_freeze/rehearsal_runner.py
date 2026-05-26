from typing import Optional, List
from usa_signal_bot.provider_freeze.phase114_models import (
    DataLayerRehearsalReport,
    DataLayerRehearsalScenario,
    DataLayerRehearsalStep,
    DataLayerOutputContract,
    create_rehearsal_report_id,
    create_rehearsal_step_id,
    _utcnow_str
)
from usa_signal_bot.core.enums import (
    DataLayerRehearsalStatus,
    DataLayerOutputContractStatus,
    ProviderFreezeRiskFlag
)
from usa_signal_bot.provider_freeze.rehearsal_scenario_builder import build_default_rehearsal_scenarios
from usa_signal_bot.provider_freeze.output_contract_checker import check_rehearsal_step_output_contract

class DataLayerRehearsalRunner:
    def __init__(self, scenarios: Optional[List[DataLayerRehearsalScenario]] = None, output_contract: Optional[DataLayerOutputContract] = None):
        self.scenarios = scenarios or build_default_rehearsal_scenarios()
        self.output_contract = output_contract

    def run(self) -> DataLayerRehearsalReport:
        steps = []
        for s in self.scenarios:
            steps.append(self.run_scenario(s))
        return self.summarize(steps)

    def run_scenario(self, scenario: DataLayerRehearsalScenario) -> DataLayerRehearsalStep:
        step = DataLayerRehearsalStep(
            step_id=create_rehearsal_step_id(),
            created_at_utc=_utcnow_str(),
            scenario_id=scenario.scenario_id,
            step_name=scenario.name,
            status=DataLayerRehearsalStatus.RUNNING_METADATA_ONLY,
            metadata_only=True,
            dry_run_only=True
        )

        # Simulate dry run
        step.outputs = {"provider_metadata": "simulated_ok"}

        oc_status = check_rehearsal_step_output_contract(step, self.output_contract)
        step.output_contract_status = oc_status

        if oc_status == DataLayerOutputContractStatus.PASS:
            step.passed = True
            step.status = DataLayerRehearsalStatus.PASSED
            step.message = "Scenario rehearsal passed."
        else:
            step.passed = False
            step.status = DataLayerRehearsalStatus.FAILED
            step.message = "Scenario output contract failed."
            step.risk_flags.append(ProviderFreezeRiskFlag.REHEARSAL_FAILED)

        return step

    def summarize(self, steps: List[DataLayerRehearsalStep]) -> DataLayerRehearsalReport:
        report = DataLayerRehearsalReport(
            rehearsal_id=create_rehearsal_report_id(),
            created_at_utc=_utcnow_str(),
            scenarios=self.scenarios,
            steps=steps,
            total_scenarios=len(self.scenarios)
        )

        for step in steps:
            if step.status == DataLayerRehearsalStatus.PASSED:
                report.passed_scenarios += 1
            elif step.status == DataLayerRehearsalStatus.WARNING:
                report.warning_scenarios += 1
            elif step.status == DataLayerRehearsalStatus.FAILED:
                report.failed_scenarios += 1
            elif step.status == DataLayerRehearsalStatus.BLOCKED:
                report.blocked_scenarios += 1

        report.rehearsal_passed = (report.failed_scenarios == 0 and report.blocked_scenarios == 0)
        report.output_contracts_passed = report.rehearsal_passed
        report.status = DataLayerRehearsalStatus.PASSED if report.rehearsal_passed else DataLayerRehearsalStatus.FAILED

        return report

    def validate_step_safety(self, step: DataLayerRehearsalStep) -> List[str]:
        errors = []
        if not step.metadata_only:
            errors.append("Step is not metadata_only")
        if not step.dry_run_only:
            errors.append("Step is not dry_run_only")
        if step.network_used or step.paid_api_used or step.scraping_used or step.html_parsing_used or step.broker_used or step.order_created or step.paper_state_mutated or step.telegram_real_sent or step.dashboard_started:
            errors.append("Execution boundaries violated in step")
        if step.produces_trade_signal or step.produces_order_decision:
            errors.append("Step produced trade signal or order decision")
        return errors
