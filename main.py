from typing import Optional

import requests
from bs4 import BeautifulSoup

from src.informations import informations


def getsoup(url: str) -> Optional[BeautifulSoup]:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def main():
    soup = getsoup("https://www.millesima.fr/chateau-citran-2018.html")
    if soup is None:
        print("Failed to fetch the webpage.")
        return

    print(informations(soup))


if __name__ == "__main__":
    main()
