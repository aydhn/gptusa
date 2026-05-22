import re

# Fix PrePaperDryRehearsalPlan constructor
with open('usa_signal_bot/paper_pre_rehearsal/dry_rehearsal_plan.py', 'r') as f:
    content = f.read()

content = content.replace("created_at_utc=datetime.datetime.utcnow().isoformat(),", "")
with open('usa_signal_bot/paper_pre_rehearsal/dry_rehearsal_plan.py', 'w') as f:
    f.write(content)

# Fix MutationFirewallRule constructor
with open('usa_signal_bot/paper_pre_rehearsal/firewall_rules.py', 'r') as f:
    content = f.read()

content = content.replace("created_at_utc=datetime.datetime.utcnow().isoformat(),", "")
with open('usa_signal_bot/paper_pre_rehearsal/firewall_rules.py', 'w') as f:
    f.write(content)
