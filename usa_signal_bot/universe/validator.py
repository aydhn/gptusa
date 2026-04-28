from pathlib import Path
from typing import List, Optional

from usa_signal_bot.universe.models import (
    UniverseSymbol, UniverseDefinition, UniverseValidationIssue, UniverseValidationReport
)
from usa_signal_bot.universe.symbols import is_valid_symbol
from usa_signal_bot.core.exceptions import UniverseValidationError

def validate_universe_symbol(symbol: UniverseSymbol, max_length: int = 15) -> List[UniverseValidationIssue]:
    issues = []

    if not symbol.symbol:
        issues.append(UniverseValidationIssue(
            field="symbol", severity="ERROR", message="Symbol is empty", symbol=symbol.symbol
        ))
    elif not is_valid_symbol(symbol.symbol, max_length=max_length):
        issues.append(UniverseValidationIssue(
            field="symbol", severity="ERROR", message=f"Invalid symbol format: {symbol.symbol}", symbol=symbol.symbol
        ))

    if not symbol.asset_type:
        issues.append(UniverseValidationIssue(
            field="asset_type", severity="ERROR", message="Asset type is required", symbol=symbol.symbol
        ))

    return issues

def find_duplicate_symbols(symbols: List[str]) -> List[str]:
    seen = set()
    dupes = set()
    for s in symbols:
        if s in seen:
            dupes.add(s)
        else:
            seen.add(s)
    return sorted(list(dupes))

def validate_universe_definition(universe: UniverseDefinition) -> UniverseValidationReport:
    report = UniverseValidationReport(source_path=universe.created_from or "memory")
    report.total_rows = len(universe.symbols)

    symbols_list = []

    for i, sym in enumerate(universe.symbols, start=1):
        sym_issues = validate_universe_symbol(sym)
        for issue in sym_issues:
            issue.row_number = i
            report.issues.append(issue)

        if sym.symbol:
            symbols_list.append(sym.symbol)

        if sym_issues:
            report.invalid_rows += 1
        else:
            report.valid_rows += 1

    dupes = find_duplicate_symbols(symbols_list)
    report.duplicate_symbols = dupes
    if dupes:
        for d in dupes:
            report.issues.append(UniverseValidationIssue(
                field="symbol", severity="WARNING", message=f"Duplicate symbol: {d}", symbol=d
            ))

    report.passed = report.invalid_rows == 0
    return report

def validate_universe_csv_file(path: Path) -> UniverseValidationReport:
    from usa_signal_bot.universe.loader import load_universe_csv
    from usa_signal_bot.core.exceptions import UniverseLoadError

    try:
        load_result = load_universe_csv(path)
        report = validate_universe_definition(load_result.universe)

        # Merge load errors into report
        for i, err in enumerate(load_result.errors, start=1):
            report.issues.append(UniverseValidationIssue(
                field="csv_load", severity="ERROR", message=err
            ))
            report.passed = False

        return report

    except (UniverseLoadError, UniverseValidationError) as e:
        report = UniverseValidationReport(source_path=str(path), passed=False)
        report.issues.append(UniverseValidationIssue(
            field="file", severity="ERROR", message=str(e)
        ))
        return report

def assert_universe_valid(report: UniverseValidationReport) -> None:
    if not report.passed or report.invalid_rows > 0:
        raise UniverseValidationError(f"Universe validation failed for {report.source_path} with {report.invalid_rows} invalid rows.")
