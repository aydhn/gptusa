with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    content = f.read()

# Let's see if we double defined something or broke the dataclass decorator
print(content.split("class AppConfig:")[0][-200:])
print("---")
print(content.split("class AppConfig:")[1][:200])
