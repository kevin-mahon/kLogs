import logging
import argparse
import threading
from kLogger import kLogger

def test(logfile, loglevel):
    #test creation
    log = kLogger("klogs", logfile, loglevel)

    #test default usage
    log.debug("debug message")
    log.info("info message")
    log.warning("warning message")
    log.error("error message")
    log.critical("critical message")

    #test calls
    log()
    x = 10
    log(x)

def test_threads(logfile, loglevel):
    log = kLogger("klogs", logfile, loglevel)
    
    def thread():
        log.debug("debug message")
        log.info("info message")
        log.warning("warning message")
        log.error("error message")
        log.critical("critical message")

        #test calls
        log()
        x = 10
        log(x)

    print("######## In thread ########")
    t = threading.Thread(target=thread)
    t.start()
    t.join()
    print("######## Outside thread ########")
    thread()

if __name__ == "__main__":
    #argparsing 
    argparser = argparse.ArgumentParser(description='Klogs')
    argparser.add_argument('-f', '--file', help='Log file')
    argparser.add_argument('-l', '--level', help='Log level')
    args = argparser.parse_args()
    print("######## Testing normal usage ########")
    test(args.file, args.level)
    print("######## Testing threaded usage ########")
    test_threads(args.file, args.level)

