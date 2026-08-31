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


def test_color_formatter_wraps_message_in_ansi(record):
    out = kColorFormatter().format(record)

    assert kFormatter.yellow in out  # WARNING colour
    assert out.endswith(kFormatter.reset)
    assert "klogs - WARNING - something happened (mod.py:7)" in out


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


def test_nocolor_formatter_has_no_ansi_codes(record):
    out = kNoColorFormatter().format(record)

    assert "\x1b[" not in out
    assert out == "klogs - WARNING - something happened (mod.py:7)"


def test_nocolor_formatter_adds_timestamp_prefix(record):
    out = kNoColorFormatter(timestamp=True).format(record)

    assert re.match(TIMESTAMP_RE + "klogs - WARNING", out)
