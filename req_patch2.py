def check_reqs():
    with open("requirements.txt", "r") as f:
        content = f.read()

    # ensure we didn't add heavy ML libs
    forbidden = ["sklearn", "scipy", "statsmodels", "hmmlearn", "tslearn"]
    for fb in forbidden:
        if fb in content:
            print(f"Error: Forbidden dependency {fb} found in requirements.txt")
            return

    print("Dependencies OK")

check_reqs()
