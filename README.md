# autojoin

Simple utility to join split files.  Run with Python 3 in a directory
containing files with names such as example.avi.001, example.avi.002,
etc.  If everything goes well, those files will be joined into the
original example.avi and the split pieces deleted.


NOTE: This software was written quickly for personal use and currently lacks
comprehensive error checking, unit tests, and other niceities which software
written for public distribution should include.  Please review the code
before running.  By default it WILL delete the source split parts so data
loss is a real possibility.  You have been warned.
