def prix(soup):
    price_blocks = soup.select('div[data-rbf="millesima-price"]')
    if len(price_blocks) < 2:
        return None

    price_tag = price_blocks[1].select_one("span")
    if price_tag:
        price_raw = price_tag.get_text()
        price_str = price_raw.split()[0].replace(",", ".")
        try:
            return float(price_str)
        except ValueError:
            return None

    return None
