import re

with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    lines = f.readlines()

out_lines = []
skip = False
for line in lines:
    if "@dataclass\n" in line and "class MultiTimeframeRegimeConfig:" in "".join(lines):
         # It's there.
         pass
    if "class MultiTimeframeRegimeConfig:" in line:
         skip = True
    if skip and "class CostRobustnessNotificationsConfig:" in line:
         skip = False
    if not skip:
        out_lines.append(line)

# Let's just restore the file from Git and apply the changes cleanly
