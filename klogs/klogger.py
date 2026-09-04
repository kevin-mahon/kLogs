import inspect
import logging

from executing import Source

from .kfilter import kFilter
from .kformatter import kColorFormatter, kNoColorFormatter


class _ExcludeFilterAdapter(logging.Filter):
    """Bridges a kFilter into the stdlib logging.Filter contract.

    kFilter.filter(msg) returns True when msg matches the filter's
    exclude condition, but logging.Filter.filter(record) returns True
    when the record should be *kept* — so the result is inverted here.

    The record is rendered with record.getMessage() rather than
    record.msg, so %-style args are substituted in first: a filter for
    "teststring" correctly matches log.debug("test %s", "teststring"),
    which would otherwise only ever see the raw "test %s" template.
    """

    def __init__(self, kfilter: kFilter):
        super().__init__()
        self.kfilter = kfilter

    def filter(self, record: logging.LogRecord) -> bool:
        return not self.kfilter.filter(record.getMessage())


class kLogger:
    def __init__(self, tag, logfile=None, loglevel="DEBUG", timestamp=False):
        if not loglevel:
            loglevel = "DEBUG"
        self.tag = tag
        self.logfile = logfile
        self.loglevel = loglevel
        self.logger = logging.getLogger(self.tag)
        self.logger.setLevel(self.loglevel.upper())

        if not self.logfile:
            self.ch = logging.StreamHandler()
            self.ch.setFormatter(kColorFormatter(timestamp))
        else:
            self.ch = logging.FileHandler(self.logfile)
            self.ch.setFormatter(kNoColorFormatter(timestamp))
        self.ch.setLevel(self.loglevel.upper())

        if not self.logger.handlers:
            self.logger.addHandler(self.ch)

    def __call__(self, *args):
        if args:
            currentframe = inspect.currentframe()
            callFrame = currentframe.f_back if currentframe is not None else None
            if callFrame:
                callNode = Source.executing(callFrame).node
                source = Source.for_frame(callFrame)
                for i, arg in enumerate(args):
                    expression = source.asttokens().get_text(callNode.args[i])
                    self.logger.info(f"{expression} | {arg}", stacklevel=2)
        else:
            self.logger.info("", stacklevel=2)

    def debug(self, message, *args, **kwargs):
        self.logger.debug(message, *args, stacklevel=2, **kwargs)

    def info(self, message, *args, **kwargs):
        self.logger.info(message, *args, stacklevel=2, **kwargs)

    def warning(self, message, *args, **kwargs):
        self.logger.warning(message, *args, stacklevel=2, **kwargs)

    def error(self, message, *args, **kwargs):
        self.logger.error(message, *args, stacklevel=2, **kwargs)

    def critical(self, message, *args, **kwargs):
        self.logger.critical(message, *args, stacklevel=2, stack_info=True, **kwargs)

    def setLevel(self, level):
        if level:
            self.loglevel = level.upper()
            self.logger.setLevel(level.upper())
            self.ch.setLevel(level.upper())

    def setFile(self, file):
        if file:
            self.logfile = file
            self.logger.handlers.clear()
            self.logger.setLevel(self.loglevel.upper())

            self.ch = logging.FileHandler(self.logfile)
            self.ch.setFormatter(kNoColorFormatter())
            self.ch.setLevel(self.loglevel.upper())
            self.logger.addHandler(self.ch)

    def addFile(self, file):
        ch = logging.FileHandler(file)
        ch.setFormatter(kNoColorFormatter())
        ch.setLevel(self.loglevel.upper())
        self.logger.addHandler(ch)

    def addFilter(self, kfilter: kFilter):
        """Drop records whose formatted message matches kfilter, across
        every handler (stream and any files added via addFile/setFile)."""
        self.logger.addFilter(_ExcludeFilterAdapter(kfilter))


def get_logger(tag, timestamp=False, logfile=None, loglevel=None):
    return kLogger(tag, logfile, loglevel, timestamp)
