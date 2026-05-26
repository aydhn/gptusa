import sys
try:
    from usa_signal_bot.core.config_schema import Config
    print("Config imported OK")
    sys.exit(0)
except Exception as e:
    import traceback
    traceback.print_exc()
    print("Error:", e)
    sys.exit(1)
