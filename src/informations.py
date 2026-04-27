from src.appellation import appellation
from src.notation import parker, robinson, suckling
from src.prix import prix


def informations(soup):
    appellation_res = appellation(soup)
    parker_res = parker(soup)
    robinson_res = robinson(soup)
    suckling_res = suckling(soup)
    prix_res = prix(soup)

    return f"{appellation_res},{parker_res},{robinson_res},{suckling_res},{prix_res}"
