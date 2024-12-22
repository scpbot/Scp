def get(directory):
    with open(f"{directory}/.version") as f:
        version = f.read().rstrip("\n").rstrip("\r")
    return version
