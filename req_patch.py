def update_reqs():
    with open("requirements.txt", "r") as f:
        content = f.read()

    if "pandas" not in content:
        content += "\npandas\n"
        with open("requirements.txt", "w") as f:
            f.write(content)

update_reqs()
