import logging
from typing import ClassVar


class kFormatter(logging.Formatter):
    grey = "\x1b[34;20m"
    blue = "\x1b[38;20m"
    yellow = "\x1b[36;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[41;1m"
    reset = "\x1b[0m"
    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"


class kColorFormatter(kFormatter):
    # format dictionary
    FORMATS : ClassVar[dict] = {
        logging.DEBUG: kFormatter.grey,
        logging.INFO: kFormatter.blue,
        logging.WARNING: kFormatter.yellow,
        logging.ERROR: kFormatter.red,
        logging.CRITICAL: kFormatter.bold_red,
    }

    def __init__(self, timestamp=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp_flag = timestamp

    def format(self, record):
        color_fmt = self.FORMATS.get(record.levelno)
        if self.timestamp_flag:
            formatter = logging.Formatter(
                color_fmt + "%(asctime)s: " + kFormatter.format + kFormatter.reset,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        else:
            formatter = logging.Formatter(
                color_fmt + kFormatter.format + kFormatter.reset
            )
        return formatter.format(record)


class kNoColorFormatter(kFormatter):
    def __init__(self, timestamp=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp_flag = timestamp

    def format(self, record):
        if self.timestamp_flag:
            formatter = logging.Formatter(
                "%(asctime)s: " + kFormatter.format, datefmt="%Y-%m-%d %H:%M:%S"
            )
        else:
            formatter = logging.Formatter(kFormatter.format)
        return formatter.format(record)
