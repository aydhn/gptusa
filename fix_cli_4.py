with open('usa_signal_bot/app/cli.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.strip() == 'elif args.command == "taskqueue-info":':
        new_lines.append('        elif args.command == "taskqueue-info":\n')
    else:
        new_lines.append(line)

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.writelines(new_lines)
