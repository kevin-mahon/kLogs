# kLogs
Small logging utility for uniform format, color, and some helper scripts to add to files in directory.

Copy to your directory and call:
```
python klogs.py -p .
```
To add the import and log to each directory

You can use like so:
```
    log = klogs.kLogger(level, outfile)
    log.debug("debug statement")
    log.info("info statement")
    log.warning("warning statement")
    log.error("error statement")
    log.critical("critical statement")
```
or if you ran the command above (to add to directory) you can simply just use the log in your files without creating
the kLogger object.

When trying to set the debug level across the entire system you can do so via:
```
    import foo
    import bar
 
    foo.log.setLevel("debug")
    bar.log.setLevel("info")
    foo.log.setFile("foo.log")
    bar.log.setFile("bar.log")
```
