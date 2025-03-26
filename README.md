# kLogs
Small logging utility for uniform format, color

Docs are WIP

You can use like so:
```python
    log = klogs.kLogger(level, outfile)
    log.debug("debug statement")
    log.info("info statement")
    log.warning("warning statement")
    log.error("error statement")
    log.critical("critical statement")
```
```none
\x1b[34;20mklogs - DEBUG - debug message (klogs.py:7)
klogs - INFO - info message (klogs.py:8)
klogs - WARNING - warning message (klogs.py:9)
klogs - ERROR - error message (klogs.py:10)
klogs - CRITICAL - critical message (klogs.py:11)
Stack (most recent call last):
  File "/Users/kevin/coding/kLogs/src/klogs.py", line 26, in <module>
    test(args.file, args.level)
  File "/Users/kevin/coding/kLogs/src/klogs.py", line 11, in test
    log.critical("critical message")

```

Or 

```python
    log()
    x = 10
    log(x)
```

Which will produce:
```
   klogs - INFO -  (klogs.py:12)
   klogs - INFO - x | 10 (klogs.py:14)
```
 

## Features:
- [ ] Easy to use log format language
- [ ] Search
- [ ] Open source at line
- [ ] log and assert

## Installation
WIP

## Usage
WIP
