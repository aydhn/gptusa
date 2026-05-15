with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# Make sure AppConfig is decorated with @dataclass
content = content.replace("class AppConfig:", "@dataclass\nclass AppConfig:")

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.write(content)
