from src.appellation import appellation
from src.notation import robert, parker, robinson, suckling
from src.prix import prix


def informations(soup, isparker):
    appellation_res = appellation(soup)
    parkerrobert_res = None
    if(isparker):
        parkerrobert_res== parker(soup)
    else:
        parkerrobert_res = robert(soup)
    robinson_res = robinson(soup)
    suckling_res = suckling(soup)
    prix_res = prix(soup)

    return f"{appellation_res},{parkerrobert_res},{robinson_res},{suckling_res},{prix_res}"
