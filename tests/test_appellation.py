import json

from bs4 import BeautifulSoup

from src.appellation import appellation


def test_appellation_returns_value():
    # Test that the function correctly extracts the value when the script exists
    data = {
        "props": {
            "pageProps": {
                "initialReduxState": {
                    "product": {
                        "content": {
                            "attributes": {"appellation": {"value": "Test Appellation"}}
                        }
                    }
                }
            }
        }
    }
    html = f'<script id="__NEXT_DATA__">{json.dumps(data)}</script>'
    soup = BeautifulSoup(html, "html.parser")

    # The function should return the correct appellation value
    assert appellation(soup) == "Test Appellation"


def test_appellation_no_script():
    # Test the case where there is no script tag with the expected id
    html = "<html></html>"
    soup = BeautifulSoup(html, "html.parser")

    # The function should return None if the script tag is missing
    assert appellation(soup) is None


def test_appellation_empty_script():
    # Test the case where the script tag exists but is empty
    html = '<script id="__NEXT_DATA__"></script>'
    soup = BeautifulSoup(html, "html.parser")

    # The function should return None if the script has no content
    assert appellation(soup) is None
