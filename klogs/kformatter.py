import logging
import os
import sys
from typing import ClassVar


class kFormatter(logging.Formatter):
    grey = "\x1b[34;20m"
    blue = "\x1b[38;20m"
    yellow = "\x1b[36;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[41;1m"
    dim = "\x1b[2m"
    reset = "\x1b[0m"

    # Pad levelname to this width so the " - " separator lands in the same
    # column no matter how long the level name is (DEBUG vs WARNING vs CRITICAL).
    LEVEL_WIDTH = len("CRITICAL")

    @staticmethod
    def location(record: logging.LogRecord) -> str:
        return f"({record.filename}:{record.lineno})"


def _color_enabled() -> bool:
    """Whether kColorFormatter should emit ANSI color codes.

    Honors the NO_COLOR / FORCE_COLOR conventions, and otherwise only
    colors output when stderr is an interactive terminal — so redirecting
    logs to a file or a log collector doesn't dump raw escape codes.
    """
    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    return sys.stderr.isatty()


class kColorFormatter(kFormatter):
    # format dictionary
    FORMATS: ClassVar[dict[int, str]] = {
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
        if not _color_enabled():
            return kNoColorFormatter(self.timestamp_flag).format(record)

        level_color = self.FORMATS.get(record.levelno, kFormatter.grey)
        level = f"{level_color}{record.levelname:<{kFormatter.LEVEL_WIDTH}}{kFormatter.reset}"
        location = f"{kFormatter.dim}{self.location(record)}{kFormatter.reset}"
        fmt = f"%(name)s - {level} - %(message)s {location}"

        if self.timestamp_flag:
            fmt = f"{kFormatter.dim}%(asctime)s: {kFormatter.reset}" + fmt
            formatter = logging.Formatter(fmt, datefmt="%Y-%m-%d %H:%M:%S")
        else:
            formatter = logging.Formatter(fmt)
        return formatter.format(record)


class kNoColorFormatter(kFormatter):
    def __init__(self, timestamp=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timestamp_flag = timestamp

    def format(self, record):
        level = f"{record.levelname:<{kFormatter.LEVEL_WIDTH}}"
        fmt = f"%(name)s - {level} - %(message)s {self.location(record)}"

        if self.timestamp_flag:
            formatter = logging.Formatter(
                "%(asctime)s: " + fmt, datefmt="%Y-%m-%d %H:%M:%S"
            )
        else:
            formatter = logging.Formatter(fmt)
        return formatter.format(record)
