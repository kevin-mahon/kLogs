import logging

import pytest

from klogs.kfilter import kWordFilter
from klogs.kformatter import kColorFormatter, kNoColorFormatter
from klogs.klogger import get_logger, kLogger


def test_defaults_to_colour_stream_handler(unique_tag):
    log = kLogger(unique_tag)

    assert len(log.logger.handlers) == 1
    handler = log.logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert isinstance(handler.formatter, kColorFormatter)
    assert log.logger.level == logging.DEBUG


@pytest.mark.parametrize("loglevel", ["", None])
def test_falsy_loglevel_falls_back_to_debug(unique_tag, loglevel):
    log = kLogger(unique_tag, loglevel=loglevel)

    assert log.loglevel == "DEBUG"
    assert log.logger.level == logging.DEBUG


def test_logfile_uses_plain_file_handler(unique_tag, tmp_path):
    logfile = tmp_path / "out.log"

    log = kLogger(unique_tag, logfile=str(logfile))

    handler = log.logger.handlers[0]
    assert isinstance(handler, logging.FileHandler)
    assert isinstance(handler.formatter, kNoColorFormatter)


def test_custom_loglevel_is_applied_to_logger_and_handler(unique_tag):
    log = kLogger(unique_tag, loglevel="warning")

    assert log.logger.level == logging.WARNING
    assert log.ch.level == logging.WARNING


def test_handlers_are_not_duplicated_for_a_shared_tag(unique_tag):
    first = kLogger(unique_tag)
    second = kLogger(unique_tag)

    assert first.logger is second.logger
    assert len(second.logger.handlers) == 1


def test_set_level_updates_logger_and_handler(unique_tag):
    log = kLogger(unique_tag)

    log.setLevel("error")

    assert log.loglevel == "ERROR"
    assert log.logger.level == logging.ERROR
    assert log.ch.level == logging.ERROR


def test_set_level_ignores_falsy_values(unique_tag):
    log = kLogger(unique_tag, loglevel="info")

    log.setLevel(None)

    assert log.logger.level == logging.INFO


def test_set_file_swaps_stream_handler_for_file_handler(unique_tag, tmp_path):
    logfile = tmp_path / "swap.log"
    log = kLogger(unique_tag)

    log.setFile(str(logfile))

    assert log.logfile == str(logfile)
    assert len(log.logger.handlers) == 1
    assert isinstance(log.logger.handlers[0], logging.FileHandler)


def test_add_file_appends_an_extra_handler(unique_tag, tmp_path):
    log = kLogger(unique_tag)

    log.addFile(str(tmp_path / "extra.log"))

    assert len(log.logger.handlers) == 2


def test_add_filter_drops_matching_records(unique_tag, caplog):
    log = kLogger(unique_tag)
    log.addFilter(kWordFilter("secret"))

    with caplog.at_level(logging.DEBUG, logger=unique_tag):
        log.info("this is fine")
        log.info("contains secret data")

    messages = [record.getMessage() for record in caplog.records]
    assert "this is fine" in messages
    assert "contains secret data" not in messages


def test_add_filter_accepts_a_bare_string(unique_tag, caplog):
    log = kLogger(unique_tag)
    log.addFilter("secret")

    with caplog.at_level(logging.DEBUG, logger=unique_tag):
        log.info("this is fine")
        log.info("contains secret data")

    messages = [record.getMessage() for record in caplog.records]
    assert "this is fine" in messages
    assert "contains secret data" not in messages


def test_add_filter_with_multiple_args_excludes_on_any_match(unique_tag, caplog):
    log = kLogger(unique_tag)
    log.addFilter("foo", "bar", "baz")

    with caplog.at_level(logging.DEBUG, logger=unique_tag):
        log.info("clean message")
        log.info("has foo in it")
        log.info("has bar in it")
        log.info("has baz in it")

    messages = [record.getMessage() for record in caplog.records]
    assert messages == ["clean message"]


def test_add_filter_with_an_and_combined_filter_requires_all_words(unique_tag, caplog):
    log = kLogger(unique_tag)
    log.addFilter(kWordFilter("foo") & kWordFilter("bar"))

    with caplog.at_level(logging.DEBUG, logger=unique_tag):
        log.info("has foo only")
        log.info("has bar only")
        log.info("has foo and bar")

    messages = [record.getMessage() for record in caplog.records]
    assert messages == ["has foo only", "has bar only"]


def test_add_filter_matches_against_the_formatted_message(unique_tag, caplog):
    # The filter should see the %-substituted message ("test teststring"),
    # not the raw template ("test %s"), so it must catch this record.
    log = kLogger(unique_tag)
    log.addFilter(kWordFilter("teststring"))

    with caplog.at_level(logging.DEBUG, logger=unique_tag):
        log.debug("test %s", "teststring")
        log.debug("test %s", "harmless")

    messages = [record.getMessage() for record in caplog.records]
    assert "test teststring" not in messages
    assert "test harmless" in messages


def test_str_formatting(unique_tag, caplog):
    log = kLogger(unique_tag)

    with caplog.at_level(logging.DEBUG, logger=unique_tag):
        log.debug("hello %s", "world")
        log.info("hello %s", "world")
        log.warning("hello %s", "world")
        log.error("hello %s", "world")
        log.critical("hello %s", "world")

    assert len(caplog.records) == 5
    assert caplog.records[-1].getMessage() == "hello world"
    assert caplog.records[-1].levelno == logging.CRITICAL


def test_get_logger_forwards_arguments_to_klogger(unique_tag, tmp_path):
    logfile = tmp_path / "g.log"

    log = get_logger(
        unique_tag, timestamp=True, logfile=str(logfile), loglevel="warning"
    )

    assert log.tag == unique_tag
    assert log.logfile == str(logfile)
    assert log.logger.level == logging.WARNING
    assert isinstance(log.logger.handlers[0], logging.FileHandler)
