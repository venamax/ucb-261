#!/usr/bin/python
from csv import reader
import sys


for row in reader(iter(sys.stdin.readline, '')):
    product = row[1].lower()
    
    if product=='debt collection' or product == 'mortgage':
        product = product
    else:
        product = 'other'
    if product:
        sys.stderr.write("reporter:counter:complaints:,%s,1\n"%product)
    print ('%s\t%s' % (product, 1))             ### mapper out looks like 'product' \t 1