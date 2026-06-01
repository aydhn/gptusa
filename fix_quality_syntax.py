import re
with open('usa_signal_bot/quality/data_quality_evaluator.py', 'r') as f:
    content = f.read()

content = content.replace('self.phase133_no_daemon_compliance_score = 0.0        self.phase141 = Phase141QualityScorecard()',
                          'self.phase133_no_daemon_compliance_score = 0.0\n        self.phase141 = Phase141QualityScorecard()')

with open('usa_signal_bot/quality/data_quality_evaluator.py', 'w') as f:
    f.write(content)
