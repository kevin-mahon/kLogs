import re

from klogs.klogger import kLogger

LEVELS = ["debug", "info", "warning", "error", "critical"]


def test_every_level_is_written_to_the_log_file(unique_tag, tmp_path):
    logfile = tmp_path / "app.log"
    log = kLogger(unique_tag, logfile=str(logfile), loglevel="DEBUG")

    for level in LEVELS:
        getattr(log, level)(f"{level} message")

    contents = logfile.read_text()
    for level in LEVELS:
        assert f"{level} message" in contents
        assert level.upper() in contents
    assert unique_tag in contents


def test_loglevel_filters_out_lower_severity_records(unique_tag, tmp_path):
    logfile = tmp_path / "filtered.log"
    log = kLogger(unique_tag, logfile=str(logfile), loglevel="WARNING")

    log.debug("hidden debug")
    log.info("hidden info")
    log.warning("visible warning")

    contents = logfile.read_text()
    assert "hidden" not in contents
    assert "visible warning" in contents


def test_timestamp_flag_prefixes_each_line(unique_tag, tmp_path):
    logfile = tmp_path / "ts.log"
    log = kLogger(unique_tag, logfile=str(logfile), loglevel="DEBUG", timestamp=True)

    log.info("with timestamp")

    line = logfile.read_text().strip().splitlines()[-1]
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}: ", line)


def test_add_file_mirrors_records_to_both_files(unique_tag, tmp_path):
    first = tmp_path / "first.log"
    second = tmp_path / "second.log"
    log = kLogger(unique_tag, logfile=str(first), loglevel="DEBUG")

    log.addFile(str(second))
    log.info("mirrored message")

    assert "mirrored message" in first.read_text()
    assert "mirrored message" in second.read_text()


def test_call_helper_writes_expression_and_value_to_file(unique_tag, tmp_path):
    logfile = tmp_path / "call.log"
    log = kLogger(unique_tag, logfile=str(logfile), loglevel="DEBUG")

    answer = 42
    log(answer)

    assert "answer | 42" in logfile.read_text()
