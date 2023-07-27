import logging
import argparse

def add_to_directory(path):
    import os 
    for file in os.listdir(path):
        if ".py" in file and file != "klogs.py":
            print(f"Adding kLogs to {file}")
            with open(file, "r+") as f:
                lines = f.readlines()
                lines.insert(0, "from klogs import kLogger\n")
                lines.insert(1, "TAG=__name__\n")
                lines.insert(2, "log = kLogger(tag=TAG)\n")
                f.seek(0,0)
                f.writelines(lines)

# create logger in file
class kLogger():

    def __init__(self, tag, logfile=None, loglevel="DEBUG"):
        self.tag = tag 
        self.logfile = logfile
        self.loglevel = loglevel
        self.logger = logging.getLogger(self.tag)

        if loglevel:
            self.logger.setLevel(loglevel.upper())
        else:
            self.logger.setLevel(logging.DEBUG)
        if logfile:
            self.ch = logging.FileHandler(logfile)
        else:
            self.ch = logging.StreamHandler()
        if loglevel:
            self.ch.setLevel(loglevel.upper())
        else:
            self.ch.setLevel(logging.DEBUG)

        self.ch.setFormatter(kFormatter())
        self.logger.addHandler(self.ch)

    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    def info(self, message):
        self.logger.info(message, stacklevel=2)

    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    def error(self, message):
        self.logger.error(message, stacklevel=2)

    def critical(self, message):
        self.logger.critical(message, stacklevel=2, stack_info=True)

    def setLevel(self, level):
        self.logger.setLevel(level.upper())
        self.ch.setLevel(level.upper())



# create format
class kFormatter(logging.Formatter):

    grey = "\x1b[34;20m"
    blue = "\x1b[38;20m"
    yellow = "\x1b[36;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[41;1m"
    reset = "\x1b[0m"
    format = "%(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    #format dictionary
    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: blue + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def test(logfile, loglevel):
    log = kLogger("klogs", logfile, loglevel)
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")
    log.critical("critical message")
    

if __name__ == "__main__":
    #argparsing 
    argparser = argparse.ArgumentParser(description='Klogs')
    argparser.add_argument('-t', '--test', help='Test Logger', action='store_true')
    argparser.add_argument('-f', '--file', help='Log file')
    argparser.add_argument('-l', '--level', help='Log level')
    argparser.add_argument('-p', '--path', help='Adds klogger to all .py files in path')
    args = argparser.parse_args()
    if args.test:
        test(args.file, args.level)
    elif args.path:
        add_to_directory(args.path)
