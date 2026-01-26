from typing import Optional

import requests
from bs4 import BeautifulSoup

from src.csv import init_csv, write_line
from src.informations import informations

CSV_PATH = "vins.csv"


def getsoup(url: str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def parse_bordeaux():
    parsed_vins = 0
    current_page = 1
    while parsed_vins < 90:
        soup = getsoup(f"https://www.millesima.fr/bordeaux.html?page={current_page}")
        if soup is None:
            break

        print("Parsing page: ", current_page)

        vin_blocks = soup.find_all("div", attrs={"data-rbf": "product-card-container"})

        print("Found ", len(vin_blocks), " vins")

        for vin_block in vin_blocks:
            # Select the link tag with href ending with ".html"
            vin_link_tag = vin_block.select_one('a[href$=".html"]')
            if vin_link_tag:
                url = vin_link_tag["href"]
                print(f"Parsing vin: {url}")
                vin_soup = getsoup(f"https://www.millesima.fr{url}")
                if vin_soup is None:
                    continue

                info = informations(vin_soup)

                print(f"Parsed info: {info}")

                write_line(CSV_PATH, info)
                parsed_vins += 1

        current_page += 1


def main():
    init_csv(CSV_PATH)
    parse_bordeaux()


if __name__ == "__main__":
    main()
