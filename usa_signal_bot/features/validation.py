from usa_signal_bot.core.enums import ValidationSeverity
from dataclasses import dataclass
from typing import List, Optional
import pandas as pd
import numpy as np

from usa_signal_bot.features.output_contract import FeatureRow
from usa_signal_bot.core.enums import FeatureValidationStatus
from usa_signal_bot.core.exceptions import FeatureValidationError

@dataclass
class FeatureValidationIssue:
    symbol: Optional[str]
    timeframe: Optional[str]
    feature_name: Optional[str]
    severity: str
    message: str

@dataclass
class FeatureValidationReport:
    status: FeatureValidationStatus
    total_rows: int
    total_features: int
    nan_ratio: float
    issues: List[FeatureValidationIssue]
    warnings: List[str]
    errors: List[str]

def validate_feature_rows(rows: List[FeatureRow], produced_features: List[str]) -> FeatureValidationReport:
    if not rows:
        return FeatureValidationReport(
            status=FeatureValidationStatus.EMPTY,
            total_rows=0,
            total_features=len(produced_features),
            nan_ratio=0.0,
            issues=[],
            warnings=["No feature rows generated."],
            errors=[]
        )

    issues = []
    warnings = []
    errors = []

    total_values = 0
    nan_values = 0

    for row in rows:
        if not row.symbol:
            issues.append(FeatureValidationIssue(row.symbol, row.timeframe, None, "WARNING", "Missing symbol in row"))
        if not row.timeframe:
            issues.append(FeatureValidationIssue(row.symbol, row.timeframe, None, "WARNING", "Missing timeframe in row"))
        if not row.timestamp_utc:
            issues.append(FeatureValidationIssue(row.symbol, row.timeframe, None, "WARNING", "Missing timestamp in row"))

        for feat in produced_features:
            val = row.features.get(feat)
            total_values += 1
            if val is None or pd.isna(val):
                nan_values += 1
            elif isinstance(val, (float, np.floating)):
                if np.isinf(val):
                    issues.append(FeatureValidationIssue(row.symbol, row.timeframe, feat, "ERROR", "Infinite value detected"))
                    errors.append(f"Infinite value for feature {feat} at {row.timestamp_utc}")

    nan_ratio = nan_values / total_values if total_values > 0 else 0.0

    if nan_ratio > 0.5:
        warnings.append(f"High NaN ratio: {nan_ratio:.2f}")
    if nan_ratio == 1.0:
        errors.append("All produced features are NaN")

    status = FeatureValidationStatus.VALID
    if errors:
        status = FeatureValidationStatus.INVALID
    elif warnings or issues:
        status = FeatureValidationStatus.WARNING

    return FeatureValidationReport(
        status=status,
        total_rows=len(rows),
        total_features=len(produced_features),
        nan_ratio=nan_ratio,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def validate_feature_dataframe(df: pd.DataFrame, feature_columns: List[str]) -> FeatureValidationReport:
    if df.empty:
        return FeatureValidationReport(
            status=FeatureValidationStatus.EMPTY,
            total_rows=0,
            total_features=len(feature_columns),
            nan_ratio=0.0,
            issues=[],
            warnings=["DataFrame is empty"],
            errors=[]
        )

    issues = []
    warnings = []
    errors = []

    total_values = len(df) * len(feature_columns)

    feat_df = df[feature_columns]

    nan_count = feat_df.isna().sum().sum()
    nan_ratio = nan_count / total_values if total_values > 0 else 0.0

    inf_count = np.isinf(feat_df.select_dtypes(include=[np.number])).sum().sum()
    if inf_count > 0:
        errors.append(f"Found {inf_count} infinite values")
        issues.append(FeatureValidationIssue(None, None, None, "ERROR", "Infinite values detected"))

    if "symbol" in df.columns and df["symbol"].isna().any():
        issues.append(FeatureValidationIssue(None, None, None, "WARNING", "Missing symbol in some rows"))
    if "timeframe" in df.columns and df["timeframe"].isna().any():
        issues.append(FeatureValidationIssue(None, None, None, "WARNING", "Missing timeframe in some rows"))

    if nan_ratio > 0.5:
        warnings.append(f"High NaN ratio: {nan_ratio:.2f}")
    if nan_ratio == 1.0:
        errors.append("All produced features are NaN")

    status = FeatureValidationStatus.VALID
    if errors:
        status = FeatureValidationStatus.INVALID
    elif warnings or issues:
        status = FeatureValidationStatus.WARNING

    return FeatureValidationReport(
        status=status,
        total_rows=len(df),
        total_features=len(feature_columns),
        nan_ratio=nan_ratio,
        issues=issues,
        warnings=warnings,
        errors=errors
    )

def feature_validation_report_to_text(report: FeatureValidationReport) -> str:
    lines = [
        "Feature Validation Report:",
        f"Status: {report.status.value}",
        f"Rows: {report.total_rows}, Features: {report.total_features}, NaN Ratio: {report.nan_ratio:.2f}"
    ]
    if report.errors:
        lines.append("Errors:")
        for e in report.errors:
            lines.append(f"  - {e}")
    if report.warnings:
        lines.append("Warnings:")
        for w in report.warnings:
            lines.append(f"  - {w}")

    if report.issues:
        lines.append(f"Issues ({len(report.issues)}):")
        for iss in report.issues[:10]:
            sym = iss.symbol or "ANY"
            tf = iss.timeframe or "ANY"
            feat = iss.feature_name or "ANY"
            lines.append(f"  [{iss.severity}] {sym}/{tf} - {feat}: {iss.message}")
        if len(report.issues) > 10:
            lines.append(f"  ... and {len(report.issues) - 10} more.")

    return "\n".join(lines)

def assert_features_valid(report: FeatureValidationReport, allow_warnings: bool = True) -> None:
    if report.status == FeatureValidationStatus.INVALID:
        raise FeatureValidationError(f"Features invalid. Errors: {report.errors}")
    if report.status == FeatureValidationStatus.WARNING and not allow_warnings:
        raise FeatureValidationError(f"Features have warnings and allow_warnings is False. Warnings: {report.warnings}")

def validate_momentum_feature_columns(df: pd.DataFrame, feature_columns: list[str]) -> FeatureValidationReport:
    return validate_feature_dataframe(df, feature_columns)

def detect_out_of_range_oscillators(df: pd.DataFrame, oscillator_columns: list[str], lower: float = 0.0, upper: float = 100.0) -> list[FeatureValidationIssue]:
    issues = []
    if df.empty: return issues
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and not df["symbol"].isna().all() else "UNKNOWN"
    timeframe = df["timeframe"].iloc[0] if "timeframe" in df.columns and not df["timeframe"].isna().all() else "UNKNOWN"
    for col in oscillator_columns:
        if col in df.columns:
            valid_data = df[col].dropna()
            if not valid_data.empty:
                out = valid_data[(valid_data < lower) | (valid_data > upper)]
                if not out.empty:
                    issues.append(FeatureValidationIssue(symbol=symbol, timeframe=timeframe, feature_name=col, severity="WARNING", message="Out of range"))
    return issues

def detect_extreme_momentum_values(df: pd.DataFrame, feature_columns: list[str], absolute_threshold: float = 1000.0) -> list[FeatureValidationIssue]:
    issues = []
    if df.empty: return issues
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and not df["symbol"].isna().all() else "UNKNOWN"
    timeframe = df["timeframe"].iloc[0] if "timeframe" in df.columns and not df["timeframe"].isna().all() else "UNKNOWN"
    for col in feature_columns:
        if col in df.columns:
            valid_data = df[col].dropna()
            if not valid_data.empty:
                extremes = valid_data[np.abs(valid_data) > absolute_threshold]
                if not extremes.empty:
                    issues.append(FeatureValidationIssue(symbol=symbol, timeframe=timeframe, feature_name=col, severity="WARNING", message="Extreme"))
    return issues


def validate_volatility_feature_columns(df: pd.DataFrame, feature_columns: list[str]) -> FeatureValidationReport:
    report = validate_feature_dataframe(df, feature_columns)
    issues = report.issues.copy()

    issues.extend(detect_negative_volatility_features(df, feature_columns))

    # Simple heuristic to find bollinger/keltner band groups
    cols = list(df.columns)
    for col in cols:
        if "_upper_" in col:
            prefix = col.split("_upper_")[0]
            suffix = col.split("_upper_")[1]
            mid_col = f"{prefix}_middle_{suffix}"
            low_col = f"{prefix}_lower_{suffix}"
            if mid_col in cols and low_col in cols:
                issues.extend(detect_invalid_band_order(df, col, mid_col, low_col))

    issues.extend(detect_extreme_volatility_values(df, feature_columns))

    report.issues = issues
    if any(iss.severity == "ERROR" for iss in issues):
        report.status = FeatureValidationStatus.INVALID
    elif any(iss.severity == "WARNING" for iss in issues) and report.status == FeatureValidationStatus.VALID:
        report.status = FeatureValidationStatus.WARNING

    return report

def detect_negative_volatility_features(df: pd.DataFrame, feature_columns: list[str]) -> list[FeatureValidationIssue]:
    issues = []
    if df.empty: return issues
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and not df["symbol"].isna().all() else "UNKNOWN"
    timeframe = df["timeframe"].iloc[0] if "timeframe" in df.columns and not df["timeframe"].isna().all() else "UNKNOWN"

    for col in feature_columns:
        if "atr" in col or "volatility" in col or "bandwidth" in col or "range" in col:
            if col in df.columns:
                valid_data = df[col].dropna()
                if not valid_data.empty:
                    neg = valid_data[valid_data < 0]
                    if not neg.empty:
                        issues.append(FeatureValidationIssue(symbol=symbol, timeframe=timeframe, feature_name=col, severity="ERROR", message="Negative volatility feature"))
    return issues

def detect_invalid_band_order(df: pd.DataFrame, upper_col: str, middle_col: str, lower_col: str) -> list[FeatureValidationIssue]:
    issues = []
    if df.empty: return issues
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and not df["symbol"].isna().all() else "UNKNOWN"
    timeframe = df["timeframe"].iloc[0] if "timeframe" in df.columns and not df["timeframe"].isna().all() else "UNKNOWN"

    # Check upper >= lower
    valid_data = df[[upper_col, middle_col, lower_col]].dropna()
    if not valid_data.empty:
        invalid_order = valid_data[valid_data[upper_col] < valid_data[lower_col]]
        if not invalid_order.empty:
             issues.append(FeatureValidationIssue(symbol=symbol, timeframe=timeframe, feature_name=upper_col, severity="ERROR", message="Upper band < Lower band"))

        # Check middle band bounds
        out_of_bounds = valid_data[(valid_data[middle_col] > valid_data[upper_col]) | (valid_data[middle_col] < valid_data[lower_col])]
        if not out_of_bounds.empty:
             issues.append(FeatureValidationIssue(symbol=symbol, timeframe=timeframe, feature_name=middle_col, severity="WARNING", message="Middle band outside upper/lower bounds"))

    return issues

def detect_extreme_volatility_values(df: pd.DataFrame, feature_columns: list[str], absolute_threshold: float = 1000.0) -> list[FeatureValidationIssue]:
    issues = []
    if df.empty: return issues
    symbol = df["symbol"].iloc[0] if "symbol" in df.columns and not df["symbol"].isna().all() else "UNKNOWN"
    timeframe = df["timeframe"].iloc[0] if "timeframe" in df.columns and not df["timeframe"].isna().all() else "UNKNOWN"

    for col in feature_columns:
        if col in df.columns:
            valid_data = df[col].dropna()
            if not valid_data.empty:
                extremes = valid_data[np.abs(valid_data) > absolute_threshold]
                if not extremes.empty:
                    issues.append(FeatureValidationIssue(symbol=symbol, timeframe=timeframe, feature_name=col, severity="WARNING", message="Extreme volatility value"))
    return issues
