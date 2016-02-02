#!/usr/bin/python
import sys

sys.stderr.write("reporter:counter:Mapper Counter,Calls,1\n")

for line in sys.stdin:
    line = line.split()
    for word in line:
        print '%s\t%s' % (word,1)