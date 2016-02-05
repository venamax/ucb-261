#!/usr/bin/python
from csv import reader
import sys


for row in reader(iter(sys.stdin.readline, '')):
    product = row[1].lower()
    issue = row[3].lower()
    

    if product == 'mortgage':
        bagofwords = issue.split(' ')
        for word in bagofwords:
            sys.stderr.write("reporter:counter:MortgageMapperCalls:,Calls,1\n")
            print ('%s\t%s' % (word, 1))             ### mapper out looks like 'word' \t 1