import logging

import pytest

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


def test_get_logger_forwards_arguments_to_klogger(unique_tag, tmp_path):
    logfile = tmp_path / "g.log"

    log = get_logger(
        unique_tag, timestamp=True, logfile=str(logfile), loglevel="warning"
    )

    assert log.tag == unique_tag
    assert log.logfile == str(logfile)
    assert log.logger.level == logging.WARNING
    assert isinstance(log.logger.handlers[0], logging.FileHandler)
