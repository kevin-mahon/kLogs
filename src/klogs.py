import logging
import argparse
from kLogger import kLogger

def test(logfile, loglevel):
    log = kLogger("klogs", logfile, loglevel)
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")
    log.critical("critical message")
    log()
    x = 10
    log(x)
    

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

