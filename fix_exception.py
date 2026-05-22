with open('usa_signal_bot/core/exceptions.py', 'r') as f:
    content = f.read()

if 'class USASignalBotError(Exception):' not in content:
    content = 'class USASignalBotError(Exception):\n    pass\n\n' + content

with open('usa_signal_bot/core/exceptions.py', 'w') as f:
    f.write(content)
