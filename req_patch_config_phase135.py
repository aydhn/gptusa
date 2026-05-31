import sys
import re

def patch_config():
    file_path = "usa_signal_bot/core/config.py"
    with open(file_path, "r") as f:
        content = f.read()

    # We need to make sure Config gets loaded correctly

    if "regime_final_closure" not in content and "def _parse_config" in content:
        # Patch the _parse_config function to load our new configs
        content = re.sub(
            r"return AppConfig\((.*?)\)",
            r"return AppConfig(\1,\n        regime_final_closure=RegimeFinalClosureConfig(**yaml_data.get('regime_final_closure', {})),\n        phase135_closure_policy=Phase135ClosurePolicyConfig(**yaml_data.get('phase135_closure_policy', {})),\n        phase135_artifact_chain=Phase135ArtifactChainConfig(**yaml_data.get('phase135_artifact_chain', {})),\n        phase135_freeze_seal=Phase135FreezeSealConfig(**yaml_data.get('phase135_freeze_seal', {})),\n        phase135_ml_kickoff=Phase135MLKickoffConfig(**yaml_data.get('phase135_ml_kickoff', {})),\n        phase135_notifications=Phase135NotificationsConfig(**yaml_data.get('phase135_notifications', {})))",
            content,
            flags=re.DOTALL
        )

        # also need to import the classes
        content = content.replace(
            "from usa_signal_bot.core.config_schema import AppConfig",
            "from usa_signal_bot.core.config_schema import AppConfig, RegimeFinalClosureConfig, Phase135ClosurePolicyConfig, Phase135ArtifactChainConfig, Phase135FreezeSealConfig, Phase135MLKickoffConfig, Phase135NotificationsConfig"
        )

    with open(file_path, "w") as f:
        f.write(content)

if __name__ == "__main__":
    patch_config()
