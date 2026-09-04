import pytest

from klogs.kfilter import kFilter, kWordFilter


def test_kfilter_is_abstract_and_cannot_be_instantiated():
    with pytest.raises(TypeError):
        kFilter()


def test_kwordfilter_returns_true_when_excluded_word_is_present():
    word_filter = kWordFilter("foo")

    assert word_filter.filter("some foo message") is True


def test_kwordfilter_returns_false_when_excluded_word_is_absent():
    word_filter = kWordFilter("foo")

    assert word_filter.filter("no match here") is False
