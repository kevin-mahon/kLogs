# kLogs
Small logging utility for uniform format, color, and some helper scripts to add to files in directory.

Copy to your directory and call:
python klogs.py -p .
To add the import and log to each directory

You can use like so:
```
1   log = klogs.kLogger(level, outfile)
2   log.debug("debug statement")
3   log.info("info statement")
4   log.warning("warning statement")
5   log.error("error statement")
6   log.critical("critical statement")
```
or if you ran the command above (to add to directory) you can simply just use the log in your files without creating
the kLogger object.

When trying to set the debug level across the entire system you can do so via:
```
1   import foo
2   import bar
3
4   foo.log.setLevel("debug")
5   bar.log.setLevel("info")
6   foo.log.setFile("foo.log")
7   bar.log.setFile("bar.log")
```
