#!/usr/bin/python
from csv import reader
import sys
sum_total = 0

for row in reader(iter(sys.stdin.readline, '')):
    product = row[1].lower()
    issue = row[3].lower()
    

    if product:
        bagofwords = issue.split(' ')
        for word in bagofwords:
            sum_total += 1
            sys.stderr.write("reporter:counter:MapperCalls:,Calls,1\n")
            print ('%s\t%s' % (word, 1))             ### mapper out looks like 'word' \t 1

print ('%s\t%s' % ('*', sum_total))             ### total sum to calculate frequencies
sys.stderr.write("reporter:counter:MapperCalls:,%s,1\n"%'*')