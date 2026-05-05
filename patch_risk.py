import re

with open('usa_signal_bot/risk/risk_store.py', 'r') as f:
    content = f.read()

# Add Optional to typing import if not there
if 'Optional' not in content:
    content = re.sub(r'from typing import (.+)', r'from typing import \1, Optional', content, count=1)

with open('usa_signal_bot/risk/risk_store.py', 'w') as f:
    f.write(content)
