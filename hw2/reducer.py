#!/usr/bin/python
from operator import itemgetter
import sys

current_number = None
current_count = 0
number = None

# input comes from STDIN
for line in sys.stdin:
    # remove leading and trailing whitespace
    line = line.strip()

    # parse the input we got from mapper.py
    number, count = line.split('\t', 1)

    # convert count (currently a string) to int
    try:
        count = int(count)
    except ValueError:
        # count was not a number, so silently
        # ignore/discard this line
        continue

    # this IF-switch only works because Hadoop sorts map output
    # by key (here: number) before it is passed to the reducer
    if current_number == number:
        current_count += count
    else:
        if current_number:
            # write result to STDOUT
            print ('%s\t%s' % (current_number, current_count))
        current_count = count
        current_number = number

# do not forget to output the last word if needed!
if current_number == number:
    print ('%s\t%s' % (current_number, current_count))