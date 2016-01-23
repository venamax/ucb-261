#!/usr/bin/python
import sys
# input comes from STDIN (standard input)
for line in sys.stdin:
    # remove leading and trailing whitespace
    number = line.strip()
    print ('%s\t%s' % (number, 1))