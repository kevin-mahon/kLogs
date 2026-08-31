import logging

from klogs.klogger import kLogger


def test_call_without_args_emits_an_empty_info_record(unique_tag, caplog):
    log = kLogger(unique_tag)

    with caplog.at_level(logging.INFO, logger=unique_tag):
        log()

    assert caplog.records
    assert caplog.records[-1].levelno == logging.INFO
    assert caplog.records[-1].message == ""


def test_call_with_arg_logs_the_source_expression_and_value(unique_tag, caplog):
    log = kLogger(unique_tag)
    value = 10

    with caplog.at_level(logging.INFO, logger=unique_tag):
        log(value)

    assert caplog.records[-1].message == "value | 10"
