#!/usr/bin/python
## mapper.py
## Author: Alejandro J. Rojas
## Description: mapper code for HW2.2

import sys
import re
from operator import itemgetter

             
counts = {}

for line in sys.stdin:                               ### input comes from STDIN (standard input)
    record = re.split(r'\t+', line) 
    if len(record) == 4:                             ### Take only complete records
        for i in range (2,len(record)):              ###  words in subject and content from each email
            bagofwords = re.split(" ",record[i])     ### Break each email records into words
            for word in bagofwords:
                neword = word.strip(',')             ### eliminate comas and other clean up
                neword = re.sub('^\'+','',word)
                neword = re.sub('^\-+','',neword)
                neword = re.sub('\-+$','',neword)   
                neword = re.sub('\!+$','',neword)  
                neword = re.sub('^\!+','',neword)  
                neword = re.sub('\'+','\'',neword)
                neword = re.sub('\-+','-',neword)
                print '%s\t%s\t%s\t%s' % (neword, 1,record[0], record[1]) 
                                                     ### output: word, 1, id, spam truth a
 
        
