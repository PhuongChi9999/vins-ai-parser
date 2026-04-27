import pytest

from src.to_ascii import to_ascii


def test_to_ascii():
    unicode = "1\u202f234,50"
    res = to_ascii(unicode)
    expected = "1234,50"
    assert res == expected
