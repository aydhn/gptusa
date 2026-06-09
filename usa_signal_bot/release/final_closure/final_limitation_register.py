from typing import List, Dict, Any
from usa_signal_bot.release.final_closure.phase160_models import (
    FinalLimitationRegister,
    FinalLimitationRecord,
    FinalAuditAreaKind,
    create_final_limitation_register_id,
    create_final_limitation_record_id,
    generate_timestamp
)
import hashlib
import json

def build_default_final_limitations() -> List[FinalLimitationRecord]:
    limitations = [
        ("Final delivery deployment approval değildir.", "Release", True),
        ("Live trading aktif değildir.", "Execution", True),
        ("Paper trading state mutation bu final fazda yapılmaz.", "Execution", True),
        ("Broker execution yoktur.", "Integration", True),
        ("Gerçek Telegram send yoktur.", "Notifications", True),
        ("Web scraping yoktur.", "Data", True),
        ("Ücretli API yoktur.", "Data", True),
        ("Outputlar yatırım tavsiyesi değildir.", "Governance", True),
        ("Backtest/ML/portfolio sonuçları research/governance sınırındadır.", "Research", True),
        ("Canlı kullanım için ayrı production hardening ve güvenli activation çalışması gerekir.", "Operations", True)
    ]

    records = []
    for title, area, applies in limitations:
        records.append(FinalLimitationRecord(
            limitation_id=create_final_limitation_record_id(),
            created_at_utc=generate_timestamp(),
            title=title,
            description=title,
            area_kind=FinalAuditAreaKind.PROJECT_CLOSURE,
            severity="INFO",
            applies_to_final_delivery=applies,
            not_blocking=True,
            mitigation_note="Expected boundary",
            warnings=[],
            errors=[],
            risk_flags=[],
            metadata={}
        ))
    return records

def compute_final_limitation_register_hash(register: FinalLimitationRegister) -> str:
    data = json.dumps([r.to_dict() for r in register.limitations], sort_keys=True)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def build_final_limitation_register() -> FinalLimitationRegister:
    records = build_default_final_limitations()
    blocking_count = len([r for r in records if not r.not_blocking])

    register = FinalLimitationRegister(
        register_id=create_final_limitation_register_id(),
        created_at_utc=generate_timestamp(),
        limitations=records,
        limitation_count=len(records),
        blocking_limitation_count=blocking_count,
        register_valid=blocking_count == 0,
        warnings=[],
        errors=[],
        risk_flags=[],
        metadata={}
    )

    register.register_hash = compute_final_limitation_register_hash(register)
    return register

def validate_final_limitation_register(register: FinalLimitationRegister) -> List[str]:
    errors = []
    if not register.register_valid:
        errors.append("Limitation register contains blocking items.")
    return errors

def final_limitation_register_to_text(register: FinalLimitationRegister, limit: int = 300) -> str:
    return f"Final Limitation Register: Count={register.limitation_count}, Blocking={register.blocking_limitation_count}"
