#!/usr/bin/python
## reducer.py
## Author: Alejandro J. Rojas
<<<<<<< HEAD
## Description: reducer code for HW1.3-1.4
=======
## Description: reducer code for HW1.5
>>>>>>> origin/master

import sys
import re
from itertools import groupby
from operator import itemgetter



word_tuple, id_list, word_list = [], [], []
sum_spam_records, sum_ham_records, sum_records = 0,0,0
sum_spam_words, sum_ham_words, sum_words = 0,0,0
wordcount_spam, wordcount_ham, wordcount = [], [], []

## collect user input
filenames = sys.argv[1:]

record_list, word_list, spam_list, ham_list = [], [], [], []
unique_ids, spam_unique_ids, ham_unique_ids = [], [],[]
for file in filenames:                                   ### Read data from mappers
    with open (file, "r") as myfile:
        for line in myfile.readlines():
            line = line.strip()
            data = re.split(r'\t+', line)
            if len(data) == 4:
                record_list.append((data[0], data[1], data[2], data[3]))
                word_list.append(data[0])
                unique_ids.append(data[2])
                if int(data[3]) == 1:
                    spam_list.append(data[0])
                    spam_unique_ids.append(data[2])             
                else:
                    ham_list.append(data[0])
                    ham_unique_ids.append(data[2])             


vocabulary = sorted(set(word_list))
size_vocabulary = len(vocabulary)


unique_ids = sorted(set(unique_ids))

spam_list = sorted(spam_list)
ham_list = sorted(ham_list)
word_list = sorted(word_list)



spam_unique_ids = sorted(set(spam_unique_ids))
ham_unique_ids = sorted(set(ham_unique_ids))


sum_words = len(word_list)
sum_spam_words = len(spam_list)
sum_ham_words = len(ham_list)


sum_records = len(unique_ids)
sum_spam_records = len(spam_unique_ids)
sum_ham_records = len(ham_unique_ids)


prior_spam = float(sum_spam_records)/sum_records     ## prior prob of a spam email
prior_ham = float(sum_ham_records)/sum_records       ## prior prob of a ham email

spam_wordcount, ham_wordcount = {}, {}
for term in vocabulary:
    count = 0
    for word in spam_list:
        if word == term:
            count+=1
    
    count_tuple = {
        term:count
    }
    spam_wordcount.update(count_tuple)
    
    count = 0
    for word in ham_list:
        if word == term:
            count+=1
    
    count_tuple = {
        term: count
    }
    ham_wordcount.update(count_tuple)

            
records = sorted(record_list, key=lambda record: record[2])


        
print "Summary of Data"
<<<<<<< HEAD
print '%4s'%sum_records ,'emails examined, containing %6s'%sum_words, 'words, we found %3s'%sum_count ,'matches.'
=======
print '%4s'%sum_records ,'emails examined, containing %6s'%sum_words, ' words using a vocabulary of %4s' %size_vocabulary, 'terms'
>>>>>>> origin/master

print '%30s' %'ID', '%10s' %'TRUTH', '%10s' %'CLASS','%20s' %'CUMULATIVE ACCURACY'
        
index, miss, sample_size = 0,0,0
for email, record in groupby(records, itemgetter(2)):
    cond_prob_spam, cond_prob_ham = 1,1        
    record_item = list(record)
    if index < 2:
        print record_item[index]
        index += 1
    
        for term in vocabulary:
            if term in record_item:
                count = 0
                print term,
                for i in range (len(record_item)):
                    if term == record_item[i][0]:
                        count += 1
                print count
                if count > 0:
                    for key,value in spam_wordcount.items():
                        if key == term:
                            spam_count = value
                            print spam_count
                    for key,value in ham_wordcount.items():
                        if key == term:
                            ham_count = value
                            print ham_count

                cond_prob_spam += count
                cond_prob_ham += count
#                cond_prob_spam *= ((float(spam_count)+1)/(float(sum_spam_words)+size_vocabulary))**count
#                cond_prob_ham *= ((float(ham_count)+1)/(float(sum_ham_words)+size_vocabulary))**count
        
    total_cond_prob = cond_prob_ham + cond_prob_spam
        

    p_spam = prior_spam*(cond_prob_spam/(total_cond_prob))
    p_ham = prior_ham*(cond_prob_ham/(total_cond_prob))
    
    if p_spam > p_ham:
        y_pred = 1
        
    else:
        y_pred = 0
    
    y_true = int(record_item[0][3])
    record_id = record_item[0][2]

    
    if y_pred != y_true:
        miss+= 1.0
    sample_size += 1.0
    accuracy = ((sample_size - miss)/sample_size)*100
                
    print  '%30s' %record_id, '%10s' %y_true, '%10s' %y_pred, '%18.2f %%' % accuracy, '%5.3f'%cond_prob_spam, '%5.3f'%cond_prob_ham
                    
                

             