#!/usr/bin/python
## reducer.py
## Author: Alejandro J. Rojas
## Description: reducer code for HW1.2-1.5

import sys
import re
sum_spam_records, sum_spam_words, sum_spam_count = 0,0,0
sum_ham_records, sum_ham_words, sum_ham_count = 0,0,0
sum_records,sum_words = 0,0

## collect user input
filenames = sys.argv[1:]
for file in filenames:
    with open (file, "r") as myfile:
        for line in myfile.readlines():
            if line.strip():
                factors = re.split(" ", line)
                sum_spam_count += int(factors[0])           ## sum up every time the word was found in a spam
                sum_spam_words += int(factors[3])           ## sum up all words from spams
                sum_spam_records+= int(factors[6])          ## sum up all emails labeled as spam
                sum_ham_count  += int(factors[9])           ## sum up every time the word was found in a ham
                sum_ham_words += int(factors[12])           ## sum up all words from hams
                sum_ham_records += int(factors[15])         ## sum up all emails labeled as ham
                sum_words += int(factors[18])               ## sum all words from all emails
                sum_records += int(factors[21])             ## sum all emails
                

prior_spam = float(sum_spam_records)/float(sum_records)     ## prior prob of a spam email
prior_ham = float(sum_ham_records)/float(sum_records)       ## prior prob of a ham email
prob_word_spam = float(sum_spam_count)/float(sum_spam_words)## prob of word given that email is spam
prob_word_ham = float(sum_ham_count)/float(sum_ham_words)   ## prob of word given that email is ham

##check_prior = prior_spam + prior_ham                        ## check priors -> sum to 1
##check_words = float(sum_words)/float(sum_spam_words+sum_ham_words) ## check probabilities of a word -> sum to 1
##check_spam = prob_word_spam*float(sum_spam_words)/float(sum_spam_count) ## check spam counts -> sum to 1
##check_ham = prob_word_ham*float(sum_ham_words)/float(sum_ham_count) ## check ham count -> sum to 1
sum_count = sum_spam_count+sum_ham_count

print "Summary of Data"
print '%4s'%sum_records ,'emails examined, containing ', '%6s'%sum_words, 'words, we found ','%3s'%sum_count ,'matches.'

print '%30s' %'ID', '%10s' %'TRUTH', '%10s' %'CLASS'
for file in filenames:                                      
    with open (file, "r") as myfile:
        for line in myfile.readlines():
            if line.strip():
                data = re.split(" ", line)
                record_id = data[24]
                y_true = data[27][0]
                count = int(data[0]) + int(data[9])
                p_spam = prior_spam*prob_word_spam**count
                p_ham = prior_ham*prob_word_ham**count
                if p_spam > p_ham:
                    y_pred = 1
                else:
                    y_pred = 0
                    
                print  '%30s' %record_id, '%10s' %y_true, '%10s' %y_pred
                
             