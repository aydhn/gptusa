with open('usa_signal_bot/app/cli.py', 'r') as f:
    content = f.read()

content = content.replace('action=SignalAction.BUY,', 'action=SignalAction.LONG,')

with open('usa_signal_bot/app/cli.py', 'w') as f:
    f.write(content)
