# kLogs

Small logging utility for uniform format, color

## Features:
- [ ] Easy to use log format language
- [ ] Search
- [ ] Open source at line
- [ ] log and assert

## Installation
```
pip install klogs-util
```

## Usage
```python
from klogs import get_logger

log = get_logger(tag, level, outfile)
log.debug("debug statement")
log.info("info statement")
log.warning("warning statement")
log.error("error statement")
log.critical("critical statement")
```
Output:
```
<tag> - DEBUG    - debug message (test.py:7)
<tag> - INFO     - info message (test.py:8)
<tag> - WARNING  - warning message (test.py:9)
<tag> - ERROR    - error message (test.py:10)
<tag> - CRITICAL - critical message (test.py:11)
Stack (most recent call last):
  File "/Users/kevin/coding/kLogs/test.py", line 26, in <module>
    test(args.file, args.level)
  File "/Users/kevin/coding/kLogs/test.py", line 11, in test
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
   <tag> - INFO     -  (test.py:12)
   <tag> - INFO     - x | 10 (test.py:14)
```

## Filters

Filters drop matching records before they reach any handler (console or file).
A record is excluded when the filter's condition matches its formatted message.

```python
from klogs import get_logger

log = get_logger("tag")

# A bare string is treated as a kWordFilter
log.addFilter("secret")
log.info("this is fine")          # printed
log.info("contains secret data")  # dropped
```

Pass several filters to exclude a record that matches **any** of them:
```python
log.addFilter("foo", "bar", "baz")
```

Combine filters explicitly with `&` (all must match) or `|` (either matches)
to build more specific conditions:
```python
from klogs.kfilter import kRegexFilter, kWordFilter

# only excluded if BOTH "foo" and "bar" are present
log.addFilter(kWordFilter("foo") & kWordFilter("bar"))

# excluded if "foo" is present OR the message looks like a phone number
log.addFilter(kWordFilter("foo") | kRegexFilter(r"\d{3}-\d{4}"))
```

Available filter classes (`klogs.kfilter`):
- `kWordFilter(exclude: str)` — matches when `exclude` is a substring of the message
- `kMultiWordFilter(exclude: list[str])` — matches when any word in the list is present
- `kRegexFilter(pattern: str)` — matches when the regex is found in the message
- `kAndFilter(*filters)` / `kOrFilter(*filters)` — combine filters (built automatically by `&` / `|`)
