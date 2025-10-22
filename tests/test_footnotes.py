import immigration_enforcement.text.footnotes as footnotes
import pytest


def test_get_abbreviations_text_returns_string():
    text = footnotes.get_abbreviations_text()
    assert isinstance(text, str)
    assert "ICE" in text and "CBP" in text


def test_get_date_footnote_text_returns_string():
    text = footnotes.get_date_footnote_text()
    assert isinstance(text, str)
    assert "11/15/2021" in text


def test_get_criminality_footnote_text_returns_string():
    text = footnotes.get_criminality_footnote_text()
    assert isinstance(text, str)
    assert "tracreports.org" in text


def test_get_date_footnote_returns_html_block():
    html = footnotes.get_date_footnote()
    assert isinstance(html, str)
    assert "ICE" in html


def test_get_criminality_footnote_returns_html_block():
    html = footnotes.get_criminality_footnote()
    assert isinstance(html, str)
    assert "convicted criminal" in html


def test_get_footnote_returns_expected_blocks():
    assert "ICE" in footnotes.get_footnote("Arresting Authority")
    assert "convicted criminal" in footnotes.get_footnote("Criminality")
    assert footnotes.get_footnote("Border Patrol") == ""


def test_get_footnote_raises_on_unknown_dataset():
    with pytest.raises(ValueError):
        footnotes.get_footnote("Banana Enforcement")
