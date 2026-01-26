import pytest
from bs4 import BeautifulSoup

from src.prix import prix


def make_html(price: float | str, text: str = ""):
    return f"""
            <div data-rbf="millesima-price">
                <span>{price} $</span>
                <span> / {text}</span>

            </div>
        """


def test_simple_price_comma():
    html = make_html(122.3) + make_html("65,80")
    soup = BeautifulSoup(html, "html.parser")
    expected = 65.8
    result = prix(soup)
    assert result == expected


def test_simple_price_dot():
    html = make_html(65.90) + make_html("65.80")
    soup = BeautifulSoup(html, "html.parser")
    expected = 65.8
    result = prix(soup)
    assert result == expected


def test_price_with_spaces():
    html = make_html(228, "TTC") + make_html("65.80      ", "unite")
    soup = BeautifulSoup(html, "html.parser")
    expected = 65.8
    result = prix(soup)
    assert result == expected


def test_price_with_tab():
    html = make_html(228) + make_html("65.80\t", "\t unite")
    soup = BeautifulSoup(html, "html.parser")
    expected = 65.8
    result = prix(soup)
    assert result == expected


def test_price_with_nbsp():
    html = make_html(228) + make_html("65.80\xa0", "\xa0 unite")
    soup = BeautifulSoup(html, "html.parser")
    expected = 65.8
    result = prix(soup)
    assert result == expected


def test_text_before_number():
    html = make_html(228) + make_html("Prix: 65,80", "unite")
    soup = BeautifulSoup(html, "html.parser")
    expected = None
    result = prix(soup)
    assert result == expected


def test_currency_before_number():
    html = make_html(228) + make_html("$65,80", "unite")
    soup = BeautifulSoup(html, "html.parser")
    expected = None
    result = prix(soup)
    assert result == expected


def test_multiple_spans_take_second():
    html = (
        make_html("422,50", "T.T.C.")
        + make_html(42.5, "unite")
        + make_html(4.5, "unite")
    )
    soup = BeautifulSoup(html, "html.parser")
    expected = 42.5
    result = prix(soup)
    assert result == expected


def test_empty_block():
    soup = BeautifulSoup('<div data-rbf="millesima-price"></div>', "html.parser")
    expected = None
    result = prix(soup)
    assert result == expected


def test_no_block():
    soup = BeautifulSoup("<div></div>", "html.parser")
    expected = None
    result = prix(soup)
    assert result == expected


def test_no_price():
    html = make_html(228) + make_html("", "unite")
    soup = BeautifulSoup(html, "html.parser")
    expected = None
    result = prix(soup)
    assert result == expected
