import logging
import re

import pytest

from klogs.kformatter import kColorFormatter, kFormatter, kNoColorFormatter

TIMESTAMP_RE = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: "


@pytest.fixture
def record():
    return logging.LogRecord(
        name="klogs",
        level=logging.WARNING,
        pathname="/somewhere/mod.py",
        lineno=7,
        msg="something happened",
        args=(),
        exc_info=None,
    )


@pytest.fixture(autouse=True)
def force_color(monkeypatch):
    """kColorFormatter only colors an interactive terminal by default; force
    it on so these tests don't depend on how pytest captures stderr."""
    monkeypatch.setenv("FORCE_COLOR", "1")
    monkeypatch.delenv("NO_COLOR", raising=False)


def test_color_formatter_colours_the_level_badge(record):
    out = kColorFormatter().format(record)

    assert f"{kFormatter.yellow}WARNING {kFormatter.reset}" in out  # WARNING colour
    assert out.endswith(kFormatter.reset)
    assert "klogs - " in out
    assert "something happened" in out


def test_color_formatter_uses_level_specific_colour(record):
    record.levelno = logging.ERROR
    record.levelname = "ERROR"

    assert kFormatter.red in kColorFormatter().format(record)


def test_color_formatter_falls_back_to_grey_for_unknown_level(record):
    record.levelno = 999

    assert kFormatter.grey in kColorFormatter().format(record)


def test_color_formatter_adds_timestamp_prefix(record):
    out = kColorFormatter(timestamp=True).format(record)

    assert re.search(TIMESTAMP_RE, out)


def test_color_formatter_dims_the_file_location(record):
    out = kColorFormatter().format(record)

    assert f"{kFormatter.dim}(mod.py:7){kFormatter.reset}" in out


def test_color_formatter_pads_level_names_for_alignment(record):
    warning_out = kColorFormatter().format(record)

    record.levelno = logging.DEBUG
    record.levelname = "DEBUG"
    debug_out = kColorFormatter().format(record)

    # the " - " separator after the level badge should land in the same
    # column regardless of how long the level name is.
    assert warning_out.index(" - something") == debug_out.index(" - something")


def test_color_formatter_respects_no_color_env_var(monkeypatch, record):
    monkeypatch.setenv("NO_COLOR", "1")

    out = kColorFormatter().format(record)

    assert "\x1b[" not in out


def test_color_formatter_disables_color_when_not_a_tty(monkeypatch, record):
    monkeypatch.delenv("FORCE_COLOR", raising=False)
    monkeypatch.setattr("sys.stderr.isatty", lambda: False)

    out = kColorFormatter().format(record)

    assert "\x1b[" not in out


def test_nocolor_formatter_has_no_ansi_codes(record):
    out = kNoColorFormatter().format(record)

    assert "\x1b[" not in out
    assert out == "klogs - WARNING  - something happened (mod.py:7)"


def test_nocolor_formatter_adds_timestamp_prefix(record):
    out = kNoColorFormatter(timestamp=True).format(record)

    assert re.match(TIMESTAMP_RE + "klogs - WARNING", out)


def test_nocolor_formatter_pads_level_names_for_alignment(record):
    warning_out = kNoColorFormatter().format(record)

    record.levelno = logging.DEBUG
    record.levelname = "DEBUG"
    debug_out = kNoColorFormatter().format(record)

    assert warning_out.index(" - something") == debug_out.index(" - something")
