def fix_test():
    with open("tests/test_phase121.py", "r") as f:
        content = f.read()

    # The outlier ratio uses a z-score threshold of 4.0 by default.
    # For a list of 4 items [1, 2, 3, 100], std is ~48, mean is ~26.5.
    # (100 - 26.5) / 48 = 1.5, which is not > 4.0.
    # We should lower the threshold or use a larger dataset.

    content = content.replace("df = pd.DataFrame({\"f1\": [1, 2, 3, 100]})", "df = pd.DataFrame({\"f1\": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1000]})")

    with open("tests/test_phase121.py", "w") as f:
        f.write(content)

fix_test()
