def to_ascii(value):
    if isinstance(value, str):
        return value.encode("ascii", "ignore").decode("ascii")
    return value