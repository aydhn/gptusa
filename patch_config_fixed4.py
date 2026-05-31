import sys

file_path = "usa_signal_bot/core/config.py"
with open(file_path, "r") as f:
    content = f.read()

# Instead of relying on specific parsing function, let's just make sure the config object instantiation has the right kwargs
# if we can find it. Wait, the instantiation is `config = AppConfig()`. Let's replace that.

if "config = AppConfig()" in content:
    content = content.replace(
        "config = AppConfig()",
        "config = AppConfig()\n        if 'regime_final_closure' in merged_cfg_dict:\n            from usa_signal_bot.core.config_schema import RegimeFinalClosureConfig\n            config.regime_final_closure = RegimeFinalClosureConfig(**merged_cfg_dict['regime_final_closure'])\n        if 'phase135_closure_policy' in merged_cfg_dict:\n            from usa_signal_bot.core.config_schema import Phase135ClosurePolicyConfig\n            config.phase135_closure_policy = Phase135ClosurePolicyConfig(**merged_cfg_dict['phase135_closure_policy'])\n        if 'phase135_artifact_chain' in merged_cfg_dict:\n            from usa_signal_bot.core.config_schema import Phase135ArtifactChainConfig\n            config.phase135_artifact_chain = Phase135ArtifactChainConfig(**merged_cfg_dict['phase135_artifact_chain'])\n        if 'phase135_freeze_seal' in merged_cfg_dict:\n            from usa_signal_bot.core.config_schema import Phase135FreezeSealConfig\n            config.phase135_freeze_seal = Phase135FreezeSealConfig(**merged_cfg_dict['phase135_freeze_seal'])\n        if 'phase135_ml_kickoff' in merged_cfg_dict:\n            from usa_signal_bot.core.config_schema import Phase135MLKickoffConfig\n            config.phase135_ml_kickoff = Phase135MLKickoffConfig(**merged_cfg_dict['phase135_ml_kickoff'])\n        if 'phase135_notifications' in merged_cfg_dict:\n            from usa_signal_bot.core.config_schema import Phase135NotificationsConfig\n            config.phase135_notifications = Phase135NotificationsConfig(**merged_cfg_dict['phase135_notifications'])"
    )

with open(file_path, "w") as f:
    f.write(content)
