import multiprocessing as mp
import threading

from klogs.klogger import kLogger


def test_records_from_a_worker_thread_and_the_main_thread_land_in_the_file(
    unique_tag, tmp_path
):
    logfile = tmp_path / "threaded.log"
    log = kLogger(unique_tag, logfile=str(logfile), loglevel="DEBUG")

    def worker():
        log.info("message from thread")

    t = threading.Thread(target=worker)
    t.start()
    t.join()
    log.info("message from main")

    contents = logfile.read_text()
    assert "message from thread" in contents
    assert "message from main" in contents


def _child(logfile, tag):
    log = kLogger(tag, logfile=logfile, loglevel="DEBUG")
    log.info("message from child process")


def test_records_from_a_child_process_and_the_parent_land_in_the_file(
    unique_tag, tmp_path
):
    logfile = tmp_path / "process.log"
    log = kLogger(unique_tag, logfile=str(logfile), loglevel="DEBUG")
    log.info("message from parent")

    ctx = mp.get_context("fork")
    proc = ctx.Process(target=_child, args=(str(logfile), unique_tag))
    proc.start()
    proc.join()

    assert proc.exitcode == 0
    contents = logfile.read_text()
    assert "message from parent" in contents
    assert "message from child process" in contents
