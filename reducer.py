#!/usr/bin/python
import sys
sum = 0
for countStr in sys.stdin:
#Look up the count value associated to each file and sum them up to get the total occurrences
    sum = sum + int(countStr)
print sum