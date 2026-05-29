import sys
import glob
import importlib.util

files = glob.glob("tests/test_*130*.py") + \
        glob.glob("tests/test_behavior*.py") + \
        glob.glob("tests/test_market_behavior*.py") + \
        glob.glob("tests/test_regime_behavior*.py") + \
        glob.glob("tests/test_diagnostics_inter*.py") + \
        glob.glob("tests/test_cross_symb*.py") + \
        glob.glob("tests/test_regime_transition_ingestion.py") + \
        glob.glob("tests/test_diagnostics_artifact_loader.py")

fails = 0
passes = 0
for file in files:
    name = file.replace("/", ".").replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for func_name in dir(mod):
        if func_name.startswith("test_") and callable(getattr(mod, func_name)):
            try:
                # We mock tmp_path for those that need it
                import inspect
                sig = inspect.signature(getattr(mod, func_name))
                if 'tmp_path' in sig.parameters:
                    from pathlib import Path
                    import tempfile
                    getattr(mod, func_name)(Path(tempfile.mkdtemp()))
                else:
                    getattr(mod, func_name)()
                passes += 1
            except Exception as e:
                fails += 1
                print(f"FAILED: {file}::{func_name}: {e}")

print(f"Passes: {passes}, Fails: {fails}")
if fails > 0:
    sys.exit(1)
