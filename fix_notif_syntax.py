with open('usa_signal_bot/notifications/notification_templates.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "from usa_signal_bot.core.enums import NotificationType" in line and not line.startswith("    "):
        new_lines.append("    from usa_signal_bot.core.enums import NotificationType\n")
    else:
        new_lines.append(line)

with open('usa_signal_bot/notifications/notification_templates.py', 'w') as f:
    f.writelines(new_lines)
