import re

# Fix PrePaperDryRehearsalPlan constructor
with open('usa_signal_bot/paper_pre_rehearsal/dry_rehearsal_plan.py', 'r') as f:
    content = f.read()

content = content.replace("plan_id=create_pre_paper_plan_id(),", "")
with open('usa_signal_bot/paper_pre_rehearsal/dry_rehearsal_plan.py', 'w') as f:
    f.write(content)

# Fix MutationFirewallRule constructor
with open('usa_signal_bot/paper_pre_rehearsal/firewall_rules.py', 'r') as f:
    content = f.read()

content = content.replace("rule_id=create_mutation_firewall_rule_id(),", "")
with open('usa_signal_bot/paper_pre_rehearsal/firewall_rules.py', 'w') as f:
    f.write(content)
