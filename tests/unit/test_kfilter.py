import pytest

from klogs.kfilter import (
    as_filter,
    kAndFilter,
    kFilter,
    kMultiWordFilter,
    kOrFilter,
    kRegexFilter,
    kWordFilter,
)


def test_kfilter_is_abstract_and_cannot_be_instantiated():
    with pytest.raises(TypeError):
        kFilter()


def test_kwordfilter_returns_true_when_excluded_word_is_present():
    word_filter = kWordFilter("foo")

    assert word_filter.filter("some foo message") is True


def test_kwordfilter_returns_false_when_excluded_word_is_absent():
    word_filter = kWordFilter("foo")

    assert word_filter.filter("no match here") is False


def test_kmultiwordfilter_returns_true_when_any_word_is_present():
    word_filter = kMultiWordFilter(["foo", "bar"])

    assert word_filter.filter("contains bar somewhere") is True


def test_kmultiwordfilter_returns_false_when_no_word_is_present():
    word_filter = kMultiWordFilter(["foo", "bar"])

    assert word_filter.filter("no match here") is False


def test_kregexfilter_returns_true_on_match():
    regex_filter = kRegexFilter(r"\d{3}-\d{4}")

    assert regex_filter.filter("call 555-1234 now") is True


def test_kregexfilter_returns_false_when_no_match():
    regex_filter = kRegexFilter(r"\d{3}-\d{4}")

    assert regex_filter.filter("no phone number here") is False


def test_kandfilter_returns_true_only_when_all_children_match():
    combined = kAndFilter(kWordFilter("foo"), kWordFilter("bar"))

    assert combined.filter("foo and bar") is True
    assert combined.filter("only foo") is False


def test_kandfilter_with_no_children_returns_true():
    assert kAndFilter().filter("anything") is True


def test_korfilter_returns_true_when_any_child_matches():
    combined = kOrFilter(kWordFilter("foo"), kWordFilter("bar"))

    assert combined.filter("only foo") is True
    assert combined.filter("only bar") is True
    assert combined.filter("neither") is False


def test_korfilter_with_no_children_returns_false():
    assert kOrFilter().filter("anything") is False


def test_filters_compose_with_each_other():
    combined = kAndFilter(
        kOrFilter(kWordFilter("foo"), kWordFilter("bar")),
        kRegexFilter(r"\d+"),
    )

    assert combined.filter("foo 123") is True
    assert combined.filter("foo only") is False
    assert combined.filter("baz 123") is False


def test_as_filter_wraps_a_bare_string_in_kwordfilter():
    wrapped = as_filter("foo")

    assert isinstance(wrapped, kWordFilter)
    assert wrapped.filter("has foo in it") is True


def test_as_filter_passes_through_an_existing_kfilter():
    original = kWordFilter("foo")

    assert as_filter(original) is original


def test_and_operator_builds_a_kandfilter():
    combined = kWordFilter("foo") & kWordFilter("bar")

    assert isinstance(combined, kAndFilter)
    assert combined.filter("foo and bar") is True
    assert combined.filter("only foo") is False


def test_or_operator_builds_a_korfilter():
    combined = kWordFilter("foo") | kWordFilter("bar")

    assert isinstance(combined, kOrFilter)
    assert combined.filter("only foo") is True
    assert combined.filter("neither") is False


def test_and_or_operators_coerce_a_bare_string_operand():
    and_combined = kWordFilter("foo") & "bar"
    or_combined = kWordFilter("foo") | "bar"

    assert and_combined.filter("foo bar") is True
    assert and_combined.filter("foo only") is False
    assert or_combined.filter("bar only") is True


def test_and_or_operators_work_with_the_string_on_the_left():
    and_combined = "foo" & kWordFilter("bar")
    or_combined = "foo" | kWordFilter("bar")

    assert and_combined.filter("foo bar") is True
    assert or_combined.filter("bar only") is True
