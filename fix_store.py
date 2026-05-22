import re

with open('usa_signal_bot/paper_admission_review/admission_review_models.py', 'r') as f:
    content = f.read()

match = re.search(r'def admission_review_full_report_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def admission_review_full_report_to_dict(item: AdmissionReviewFullReport) -> dict:
    return {
        "report_id": getattr(item, "report_id", None),
        "created_at_utc": getattr(item, "created_at_utc", None),
        "report_type": getattr(item, "report_type", None)
    }"""
    content = content.replace(block, new_block)

match = re.search(r'def paper_mode_admission_review_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def paper_mode_admission_review_to_dict(item: PaperModeAdmissionReview) -> dict:
    return {"admission_review_id": getattr(item, "admission_review_id", None)}"""
    content = content.replace(block, new_block)

match = re.search(r'def ledger_reconciliation_report_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def ledger_reconciliation_report_to_dict(item: LedgerReconciliationReport) -> dict:
    return {"reconciliation_id": getattr(item, "reconciliation_id", None)}"""
    content = content.replace(block, new_block)

match = re.search(r'def final_no_write_transition_checkpoint_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def final_no_write_transition_checkpoint_to_dict(item: FinalNoWriteTransitionCheckpoint) -> dict:
    return {"checkpoint_id": getattr(item, "checkpoint_id", None)}"""
    content = content.replace(block, new_block)

match = re.search(r'def admission_evidence_seal_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def admission_evidence_seal_to_dict(item: AdmissionEvidenceSeal) -> dict:
    return {"seal_id": getattr(item, "seal_id", None)}"""
    content = content.replace(block, new_block)

match = re.search(r'def admission_review_gate_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def admission_review_gate_to_dict(item: AdmissionReviewGate) -> dict:
    return {"gate_id": getattr(item, "gate_id", None)}"""
    content = content.replace(block, new_block)

match = re.search(r'def admission_review_audit_entry_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def admission_review_audit_entry_to_dict(item: AdmissionReviewAuditEntry) -> dict:
    return {"audit_id": getattr(item, "audit_id", None)}"""
    content = content.replace(block, new_block)

match = re.search(r'def ledger_reconciliation_item_to_dict.*?return to_dict\(item\)', content, re.MULTILINE | re.DOTALL)
if match:
    block = match.group(0)
    new_block = """def ledger_reconciliation_item_to_dict(item: LedgerReconciliationItem) -> dict:
    return {"item_id": getattr(item, "item_id", None)}"""
    content = content.replace(block, new_block)

with open('usa_signal_bot/paper_admission_review/admission_review_models.py', 'w') as f:
    f.write(content)
