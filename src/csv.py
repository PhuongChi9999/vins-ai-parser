def init_csv(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write("Appellation,Parker,J.Robinson,J.Suckling,Prix\n")


def write_line(path, line):
    with open(path, "a", encoding="utf-8") as f:
        f.write(line.strip() + "\n")
