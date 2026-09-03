import inspect
import logging

from executing import Source

from .kformatter import kColorFormatter, kNoColorFormatter


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
            for arg in args:
                currentframe = inspect.currentframe()
                callFrame = currentframe.f_back if currentframe is not None else None
                if callFrame:
                    callNode = Source.executing(callFrame).node
                    source = Source.for_frame(callFrame)
                    expression = source.asttokens().get_text(callNode.args[0])
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


def get_logger(tag, timestamp=False, logfile=None, loglevel=None):
    return kLogger(tag, logfile, loglevel, timestamp)
