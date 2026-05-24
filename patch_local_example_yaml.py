with open("config/local.example.yaml", "r") as f:
    content = f.read()

new_config = """
advanced_runtime:
  enabled: true
"""

if "advanced_runtime:" not in content:
    content = content + "\n" + new_config + "\n"
    with open("config/local.example.yaml", "w") as f:
        f.write(content)
