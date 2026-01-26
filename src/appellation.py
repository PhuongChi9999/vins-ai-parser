import json
from typing import Optional

from bs4 import BeautifulSoup


def appellation(soup: BeautifulSoup) -> Optional[str]:
    script = soup.find("script", {"id": "__NEXT_DATA__"})
    if not script or not script.string:
        return None

    data = json.loads(script.string)
    # Table is built by Next.js. We have no access to table data. So we need to parse it manually.
    return data["props"]["pageProps"]["initialReduxState"]["product"]["content"][
        "attributes"
    ]["appellation"]["value"]
