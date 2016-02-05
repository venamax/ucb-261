#!/usr/bin/python
import sys
# record mapper invokation
sys.stderr.write("reporter:counter:custom_counters,mapper_count,1\n")
max_basket = 0
num_items = 0


# input comes from STDIN
for line in sys.stdin:
    line = line.strip().lower()
    if line == '': continue
    records = line.split(' ')
    # record largest basket per mapper
    if len(records) > max_basket:
        max_basket = len(records)
    for product in records:
        num_items += 1
        print '%s\t%s' % (product, 1)

# print total word count from this mapper to calculate relative frequency
print '%s\t%s' % ('*', num_items)
# print additional meta data for EDA analysis
print '%s\t%s' % ('max_basket', max_basket)