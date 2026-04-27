import re


def prix(soup): 
    price_blocks = soup.select('div[data-rbf="millesima-price"]')
    if not price_blocks:
        return None

    i = 0 if len(price_blocks) == 1 else 1
    price_tag = price_blocks[i].select_one("span")
    if price_tag:
        price_raw: str = price_tag.get_text()
        price_str = re.sub(r"[^\d,.]", "", price_raw).replace(",", ".")
        try:
            return float(price_str)
        except ValueError:
            return None

    return None
