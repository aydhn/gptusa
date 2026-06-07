import hashlib
from typing import Any
from usa_signal_bot.backtesting.closure.phase152_models import (
    BacktestBandClosureCertificate, BacktestFinalAuditReport,
    ClosureComplianceStatus, BacktestClosureRiskFlag
)

def compute_backtest_band_closure_certificate_hash(certificate: BacktestBandClosureCertificate) -> str:
    content = f"{certificate.final_audit_report_id}_{certificate.closed}_{certificate.start_phase}_{certificate.end_phase}"
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def build_backtest_band_closure_certificate(final_audit_report: BacktestFinalAuditReport) -> BacktestBandClosureCertificate:
    cert = BacktestBandClosureCertificate()
    cert.final_audit_report_id = final_audit_report.report_id
    cert.acceptance_summary_id = final_audit_report.acceptance_summary.summary_id

    cert.closed = final_audit_report.final_audit_passed
    cert.closure_status = ClosureComplianceStatus.PASSED if cert.closed else ClosureComplianceStatus.FAILED

    if cert.closed:
        cert.ready_for_phase153 = True
    else:
        cert.risk_flags.append(BacktestClosureRiskFlag.CLOSURE_CERTIFICATE_INVALID)
        cert.errors.append("Cannot close band: final audit failed")

    cert.closure_hash = compute_backtest_band_closure_certificate_hash(cert)

    return cert

def validate_backtest_band_closure_certificate(certificate: BacktestBandClosureCertificate) -> list[str]:
    errors = []
    if not certificate.closed:
        errors.append("Certificate indicates band is not closed")
    return errors

def backtest_band_closure_certificate_summary(certificate: BacktestBandClosureCertificate) -> dict[str, Any]:
    return {"closed": certificate.closed, "ready_for_phase153": certificate.ready_for_phase153}

def backtest_band_closure_certificate_to_text(certificate: BacktestBandClosureCertificate, limit: int = 300) -> str:
    return f"BacktestBandClosureCertificate(closed={certificate.closed}, ready153={certificate.ready_for_phase153})"
