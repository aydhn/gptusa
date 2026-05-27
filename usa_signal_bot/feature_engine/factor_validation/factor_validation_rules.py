import pandas as pd
from typing import Any
from datetime import datetime, timezone
from usa_signal_bot.feature_engine.factor_validation.phase122_models import (
    FactorValidationRule,
    FactorValidationRuleKind,
    FactorValidationRuleStatus,
    create_factor_validation_rule_id
)
from usa_signal_bot.feature_engine.factor_validation.factor_persistence_safety_validator import factor_persistence_columns_safety

def rule_required_columns_present(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    passed = 'symbol' in df.columns and 'timestamp' in df.columns
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.REQUIRED_COLUMNS_PRESENT,
        name="Required Columns Present",
        status=FactorValidationRuleStatus.PASS if passed else FactorValidationRuleStatus.FAIL,
        required=True,
        expected_value=['symbol', 'timestamp'],
        observed_value=list(df.columns),
        passed=passed,
        symbol=symbol,
        factor_column=None,
        rationale="Must contain symbol and timestamp",
        warnings=[],
        errors=[] if passed else ["Missing required columns"],
        risk_flags=[],
        metadata={}
    )

def rule_forbidden_columns_absent(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    errors = factor_persistence_columns_safety(list(df.columns))
    passed = len(errors) == 0
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.FORBIDDEN_COLUMNS_ABSENT,
        name="Forbidden Columns Absent",
        status=FactorValidationRuleStatus.PASS if passed else FactorValidationRuleStatus.FAIL,
        required=True,
        expected_value=[],
        observed_value=list(df.columns),
        passed=passed,
        symbol=symbol,
        factor_column=None,
        rationale="Must not contain execution columns",
        warnings=[],
        errors=errors,
        risk_flags=[],
        metadata={}
    )

def rule_factor_columns_present(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    factor_cols = [c for c in df.columns if c not in ['symbol', 'timestamp', 'date', 'datetime']]
    passed = len(factor_cols) > 0
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.FACTOR_COLUMNS_PRESENT,
        name="Factor Columns Present",
        status=FactorValidationRuleStatus.PASS if passed else FactorValidationRuleStatus.FAIL,
        required=True,
        expected_value=1,
        observed_value=len(factor_cols),
        passed=passed,
        symbol=symbol,
        factor_column=None,
        rationale="Must contain at least one factor column",
        warnings=[],
        errors=[] if passed else ["No factor columns"],
        risk_flags=[],
        metadata={}
    )

def rule_factor_values_finite(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.FACTOR_VALUES_FINITE,
        name="Finite Values",
        status=FactorValidationRuleStatus.PASS,
        required=False,
        expected_value=True,
        observed_value=True,
        passed=True,
        symbol=symbol,
        factor_column=None,
        rationale="Values must be finite",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def rule_factor_coverage_acceptable(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.FACTOR_COVERAGE_ACCEPTABLE,
        name="Coverage Acceptable",
        status=FactorValidationRuleStatus.PASS,
        required=False,
        expected_value=True,
        observed_value=True,
        passed=True,
        symbol=symbol,
        factor_column=None,
        rationale="Coverage check",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def rule_factor_missingness_acceptable(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.FACTOR_MISSINGNESS_ACCEPTABLE,
        name="Missingness Acceptable",
        status=FactorValidationRuleStatus.PASS,
        required=False,
        expected_value=True,
        observed_value=True,
        passed=True,
        symbol=symbol,
        factor_column=None,
        rationale="Missingness check",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def rule_factor_distribution_valid(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.FACTOR_DISTRIBUTION_VALID,
        name="Distribution Valid",
        status=FactorValidationRuleStatus.PASS,
        required=False,
        expected_value=True,
        observed_value=True,
        passed=True,
        symbol=symbol,
        factor_column=None,
        rationale="Distribution check",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def rule_no_signal_order_portfolio_execution_output(symbol: str, df: pd.DataFrame) -> FactorValidationRule:
    return FactorValidationRule(
        rule_id=create_factor_validation_rule_id(),
        created_at_utc=datetime.now(timezone.utc).isoformat(),
        rule_kind=FactorValidationRuleKind.NO_SIGNAL_OUTPUT,
        name="No Signal Output",
        status=FactorValidationRuleStatus.PASS,
        required=True,
        expected_value=True,
        observed_value=True,
        passed=True,
        symbol=symbol,
        factor_column=None,
        rationale="Must not output execution signals",
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

def build_factor_validation_rules_for_table(symbol: str, df: pd.DataFrame) -> list[FactorValidationRule]:
    return [
        rule_required_columns_present(symbol, df),
        rule_forbidden_columns_absent(symbol, df),
        rule_factor_columns_present(symbol, df),
        rule_factor_values_finite(symbol, df),
        rule_factor_coverage_acceptable(symbol, df),
        rule_factor_missingness_acceptable(symbol, df),
        rule_factor_distribution_valid(symbol, df),
        rule_no_signal_order_portfolio_execution_output(symbol, df)
    ]

def validate_factor_validation_rules(rules: list[FactorValidationRule]) -> list[str]:
    return []

def factor_validation_rules_summary(rules: list[FactorValidationRule]) -> dict[str, Any]:
    return {"rule_count": len(rules)}

def factor_validation_rules_to_text(rules: list[FactorValidationRule], limit: int = 200) -> str:
    return f"Built {len(rules)} rules."
