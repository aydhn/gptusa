with open('usa_signal_bot/core/enums.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if line.strip() == 'ADMISSION_REVIEW_BLOCKED = "ADMISSION_REVIEW_BLOCKED"' and line.startswith('    '):
        if line.startswith('        '):
            new_lines.append(line.replace('        ', '    ', 1))
        else:
             new_lines.append(line)
    elif "ADMISSION_REVIEW_BLOCKED" in line or "LEDGER_RECONCILIATION_BLOCKED" in line or "NO_WRITE_TRANSITION_CHECKPOINT_BLOCKED" in line:
        if line.startswith('        '):
            new_lines.append(line.replace('        ', '    ', 1))
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('usa_signal_bot/core/enums.py', 'w') as f:
    f.writelines(new_lines)
