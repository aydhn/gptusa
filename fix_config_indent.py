with open('usa_signal_bot/core/config_schema.py', 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("    feature_engine_foundation: FeatureEngineFoundationConfig") \
      or line.startswith("    phase116_feature_policy: Phase116FeaturePolicyConfig") \
      or line.startswith("    phase116_feature_scope: Phase116FeatureScopeConfig") \
      or line.startswith("    phase116_notifications: Phase116NotificationsConfig"):
        # We will insert them manually inside the Config class properly
        continue
    new_lines.append(line)

with open('usa_signal_bot/core/config_schema.py', 'w') as f:
    f.writelines(new_lines)
