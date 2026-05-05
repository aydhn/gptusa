import subprocess
print("Pre-commit check: running tests")
res = subprocess.run(["pytest", "tests/"], capture_output=True, text=True)
if res.returncode == 0:
    print("All tests passed.")
else:
    print("Tests failed.")
