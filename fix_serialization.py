def update_models():
    with open("usa_signal_bot/feature_engine/factor_scoring/phase121_models.py", "r") as f:
        content = f.read()

    content = content.replace("from usa_signal_bot.core.serialization import to_dict_with_enums", "from usa_signal_bot.core.serialization import dataclass_to_dict")
    content = content.replace("to_dict_with_enums(item)", "dataclass_to_dict(item)")

    with open("usa_signal_bot/feature_engine/factor_scoring/phase121_models.py", "w") as f:
        f.write(content)

update_models()
