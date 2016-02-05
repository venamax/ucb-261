#!/usr/bin/python
import sys
# record reducer invokation
sys.stderr.write("reporter:counter:custom_counters,reducer_count,1\n")
total_count = 0
current_issue = None
current_count = 0
largest_basket_size = 0
unique_products = set()
for line in sys.stdin:
    line = line.strip()
    if line == '': continue
    line = line.split('\t')
    product = line[0]
    count = int(line[1])
    # record largest basket
    if product == 'max_basket':
        if count > largest_basket_size:
            largest_basket_size = count
        continue
    
    # aggregate total counts
    if product == "*":
        total_count += count
    else:
        unique_products.add(product)
        if product == current_product:
            current_count += count
        else:
            if current_product != None and count != 0:
                print "%s\t%s\t%.6f" % (current_product, current_count, float(current_count)/float(total_count))
            current_product = product
            current_count = count
if current_product != None and total_count != 0:
    print "%s\t%s\t%.6f" % (current_product, current_count, float(current_count)/float(total_count))
print "----meta data below-----"
print "Total Unique Products: %s" % len(unique_products)
print "Largest Basket Size: %s" % largest_basket_size