from bs4 import BeautifulSoup

from src.notation import find_score


def make_html(name: str, score: str) -> str:
    return f"""
    <div data-rbf="wine-critic-slide">
        <span>{name}</span>
        <span>{score}</span>
    </div>
    """


def test_simple_score():
    html = make_html("Parker", "93/100")
    soup = BeautifulSoup(html, "html.parser")
    assert find_score(soup, "Parker") == 93


def test_score_with_plus():
    html = make_html("Robinson", "96+/100")
    soup = BeautifulSoup(html, "html.parser")
    assert find_score(soup, "Robinson") == 96


def test_score_range():
    html = make_html("Suckling", "90-93/100")
    soup = BeautifulSoup(html, "html.parser")
    assert find_score(soup, "Suckling") == 91.5


def test_missing_score():
    html = """
    <div data-rbf="wine-critic-slide">
        <span>Parker</span>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    assert find_score(soup, "Parker") is None


def test_missing_critic():
    html = make_html("Robinson", "95/100")
    soup = BeautifulSoup(html, "html.parser")
    # looking for a critic not in the html
    assert find_score(soup, "Parker") is None


def test_case_insensitive():
    html = make_html("j. robinson", "88/100")
    soup = BeautifulSoup(html, "html.parser")
    assert find_score(soup, "Robinson") == 88


def test_multiple_critics():
    html = make_html("Parker", "92/100") + make_html("Robinson", "87/100")
    soup = BeautifulSoup(html, "html.parser")
    assert find_score(soup, "Robinson") == 87
    assert find_score(soup, "Parker") == 92
