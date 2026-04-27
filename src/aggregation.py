def aggregate_by(vins, name):
    return vins.groupby("Appellation")[name].mean().fillna(0)


def aggregate_robert(vins):
    return aggregate_by(vins, "Robert")


def aggregate_robinson(vins):
    return aggregate_by(vins, "J.Robinson")


def aggregate_suckling(vins):
    return aggregate_by(vins, "J.Suckling")
