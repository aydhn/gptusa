import re

with open("phase113_builder.py", "r") as f:
    content = f.read()

# Fix the indentation error
content = content.replace('''        app_config_attrs = """
    provider_governance: ProviderGovernanceConfig = field(default_factory=ProviderGovernanceConfig)''', '''        app_config_attrs = """
    provider_governance: ProviderGovernanceConfig = field(default_factory=ProviderGovernanceConfig)''')

with open("phase113_builder.py", "w") as f:
    f.write(content)
