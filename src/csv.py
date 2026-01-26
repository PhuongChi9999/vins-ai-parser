def init_csv(path: str):
    with open(path, "w", encoding="utf-8") as f:
        f.write("Appellation,Parker,J.Robinson,J.Suckling,Prix\n")


def write_line(path: str, line: str):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line.strip() + "\n")
