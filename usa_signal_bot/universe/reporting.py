import json
from pathlib import Path
from typing import Optional, List

from usa_signal_bot.universe.models import UniverseDefinition, UniverseSummary, UniverseValidationReport
from usa_signal_bot.core.enums import AssetType

def summarize_universe(universe: UniverseDefinition, source_files: Optional[List[str]] = None) -> UniverseSummary:
    summary = UniverseSummary(
        name=universe.name,
        source_files=source_files or []
    )

    for sym in universe.symbols:
        summary.total_symbols += 1

        if sym.active:
            summary.active_symbols += 1
        else:
            summary.inactive_count += 1

        if sym.asset_type == AssetType.STOCK:
            summary.stock_count += 1
        elif sym.asset_type == AssetType.ETF:
            summary.etf_count += 1

        if sym.exchange:
            summary.exchanges[sym.exchange] = summary.exchanges.get(sym.exchange, 0) + 1

        if sym.sector:
            summary.sectors[sym.sector] = summary.sectors.get(sym.sector, 0) + 1

    return summary

def universe_summary_to_text(summary: UniverseSummary) -> str:
    lines = [
        f"--- Universe Summary: {summary.name} ---",
        f"Total Symbols : {summary.total_symbols}",
        f"Active        : {summary.active_symbols}",
        f"Inactive      : {summary.inactive_count}",
        f"Stocks        : {summary.stock_count}",
        f"ETFs          : {summary.etf_count}",
        "",
        "Exchanges:"
    ]

    for exch, count in sorted(summary.exchanges.items()):
        lines.append(f"  - {exch}: {count}")

    lines.append("")
    lines.append("Sectors:")
    for sector, count in sorted(summary.sectors.items()):
        lines.append(f"  - {sector}: {count}")

    if summary.source_files:
        lines.append("")
        lines.append("Source Files:")
        for sf in summary.source_files:
            lines.append(f"  - {sf}")

    return "\n".join(lines)

def validation_report_to_text(report: UniverseValidationReport) -> str:
    lines = [
        f"--- Validation Report: {report.source_path} ---",
        f"Passed        : {'YES' if report.passed else 'NO'}",
        f"Total Rows    : {report.total_rows}",
        f"Valid Rows    : {report.valid_rows}",
        f"Invalid Rows  : {report.invalid_rows}",
        f"Duplicates    : {len(report.duplicate_symbols)}",
    ]

    if report.issues:
        lines.append("")
        lines.append("Issues:")
        for issue in report.issues:
            row_str = f"Row {issue.row_number} " if issue.row_number else ""
            sym_str = f"[{issue.symbol}] " if issue.symbol else ""
            lines.append(f"  - {issue.severity}: {row_str}{sym_str}({issue.field}) {issue.message}")

    return "\n".join(lines)

def write_universe_summary_json(path: Path, summary: UniverseSummary) -> Path:
    from usa_signal_bot.core.serialization import serialize_value

    path.parent.mkdir(parents=True, exist_ok=True)

    data = serialize_value(summary)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return path
