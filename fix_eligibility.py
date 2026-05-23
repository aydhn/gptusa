import re

with open('usa_signal_bot/paper_admission_review/eligibility_checker.py', 'r') as f:
    content = f.read()

content = content.replace("AdmissionReviewRiskFlag.BLOCK", "PaperModeAdmissionReviewDecision.BLOCK")

with open('usa_signal_bot/paper_admission_review/eligibility_checker.py', 'w') as f:
    f.write(content)
