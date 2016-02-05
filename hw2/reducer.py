#!/usr/bin/python

import numpy as np
from operator import itemgetter
import sys
from itertools import groupby
import math


current_word, word = None, None                 
current_email, email = None, None          
current_y_true, y_true = None, None


sum_records, sum_spamrecords, sum_hamrecords = 0,0,0
sum_spamwords, sum_hamwords = 0,0
spam_zeroes, ham_zeroes = 0,0


emails={} #Associative array to hold email data
words={} #Associative array for word data
conf_matrix = np.zeros((2,2))

# input comes from STDIN
for line in sys.stdin:
    
    line = line.strip()                        ### remove leading and trailing whitespace
    line = line.split('\t')                    ### parse the input we got from mapper.py 
    if len(line) == 4:
    
        try:
            word = line[0]                          ### word we get from mapper.py
            count = line[1]                         ### corresponding count
            count = int(count)                      ### convert count (currently a string) to int
            email = line[2]                         ### id that identifies each email
            y_true = line[3]                        ### spam truth
            y_true = int(y_true)                    ### spam truth as an integer
        except ValueError:                          ### any error then silently                         
            continue                                ### ignore/discard this line

                                                
                                                
        if current_word == word:                    ### this IF-switch only works because Hadoop sorts map output
            current_count += count                  ### by key (here: word) before it is passed to the reducer
        
            if current_word not in words.keys():     ### initialize word count of new words
                words[current_word]={'ham_count':0,'spam_count':0}
            
            if current_email not in emails.keys():          ### initialize word counts and label of new email
                emails[current_email]={'y_true':current_y_true,'word_count':0,'words':[]} 
                sum_records +=1.0
                if current_y_true == 1:                     ### identified new email as either spam or ham
                    sum_spamrecords +=1.0               

            elif current_email in emails.keys():
                emails[current_email]['word_count'] += 1
                emails[current_email]['words'].append(current_word)### store words in email  
    
            if current_y_true == 1:                         ### if record where word is located is a spam
                current_spamcount += count         ### add to spam count of that word
                sum_spamwords += 1.0
            else:
                current_hamcount += count          ### if not add to ham count of thet word
                sum_hamwords +=1.0 

        else:
            if current_word:
                try:
                    if current_word in words.keys():
                        words[current_word]['spam_count'] += current_spamcount ### update spam count for current word 
                        words[current_word]['ham_count'] += current_hamcount ### update ham count for current word
                except ValueError:                          ### if count was not a number then silently                         
                    continue                                ### ignore/discard this line
                    
                    
            current_count = count                   ### set current count
            current_word = word                     ### set current number
            current_email = email                   ### set current id of email
            current_y_true = y_true                 ### set current spam truth
            current_spamcount, current_hamcount = 0,0
        


if current_word == word:                       ### do not forget to output the last word if needed!
    emails[current_email]['word_count'] += 1
    emails[current_email]['words'].append(current_word)### store words in email  
    words[current_word]['spam_count'] += current_spamcount ### update spam count for current word 
    words[current_word]['ham_count'] += current_hamcount ### update ham count for current word    
    


#Calculate stats for entire corpus

prior_spam= sum_spamrecords/sum_records     
prior_ham= 1 - prior_spam
vocab_count=len(words)#number of unique words in the total vocabulary
prob_spamwords = sum_spamwords/(sum_spamwords+sum_hamwords)
prob_hamwords = 1-prob_spamwords



for k,word in words.iteritems():
    ##These versions calculate conditional probabilities WITH Laplace smoothing.  
    if (word['spam_count'] + word['ham_count']) < 3:
        word['p_spam']= 1
        word['p_ham'] = 1
    else:
        word['p_spam']=(word['spam_count']+1)/(sum_spamwords+vocab_count)
        word['p_ham']=(word['ham_count']+1)/(sum_hamwords+vocab_count)
    
    #Compute conditional probabilities WITHOUT Laplace smoothing
    #word['p_spam']=(word['spam_count'])/(sum_spamwords)
    #word['p_ham']=(word['ham_count'])/(sum_hamwords)
    
    if word['p_spam'] == 0 and word['p_ham'] == 0:
        spam_zeroes +=1
        ham_zeroes +=1
        word['p_spam']= 1
        word['p_ham'] = 1
    
    elif word['p_spam'] == 0:
        spam_zeroes +=1
        word['p_ham'] = min(0.5 ** (1/word['ham_count']),0.99999999) ### back-calculates probability 
        word['p_spam']= 1-word['p_ham']              ### of the sequence of events assuming  
                                                     ### sequence is 50% likely to happen         
    elif word['p_ham'] == 0:
        ham_zeroes +=1
        word['p_spam'] = min(0.5 ** (1/word['spam_count']),0.99999999) ### Adjust probability 
        word['p_ham']= 1-word['p_spam']               ### just as above
    
    word['p_spam'] = math.log(word['p_spam'])              ### convert to log scale
    word['p_ham'] = math.log(word['p_ham'])               
        
#At this point the model is now trained, and we can use it to make our predictions

print 'Analyzed %s' % sum_records, 'using a vocabulary of %s' % vocab_count , 'terms'
print 'On %s'%spam_zeroes , 'times we found spam probabilities that were zero'
print 'On %s'%ham_zeroes, 'times we found not spam probabilities that were zero'
print '%30s' %'ID', '%10s' %'TRUTH', '%10s' %'CLASS', '%20s' %'CUMULATIVE ACCURACY', '%10s'%'P-SPAM', '%10s'%'P-HAM'
miss, sample_size = 0,0 
prob_spam_list, prob_ham_list = [], []
for j,email in emails.iteritems():
    
    #Log versions - no longer used
    p_spam= math.log(prior_spam)
    p_ham= math.log(prior_ham)
    
    #p_spam=prior_spam
    #p_ham=prior_ham
    
    for word in email['words']:

        try:
            #p_spam+=log(words[word]['p_spam']) #Log version - no longer used
            p_spam+=words[word]['p_spam']
        except ValueError:
            pass #This means that words that do not appear in a class will use the class prior
        try:
            #p_ham+=log(words[word]['p_ham']) #Log version - no longer used
            p_ham+=words[word]['p_ham']
        except ValueError:
            pass
    
    
    if p_spam>p_ham:
        y_pred=1
        
    else:
        y_pred=0
    y_true = email['y_true']
    if y_true == 1:
        prob_spam_list.append(math.exp(p_spam))
        if y_pred == 1:
            conf_matrix[0][0] +=1                     ### update confusion matrix
        else:
            conf_matrix[0][1] +=1
    else:
        prob_ham_list.append(math.exp(p_spam))
        if y_pred == 0:
            conf_matrix[1][1] +=1
        else:
            conf_matrix[1][0] +=1
    
    
    if y_pred != y_true:
        miss+= 1.0
        
    sample_size += 1.0
    accuracy = ((sample_size-miss)/sample_size)*100
    prob_spam = math.exp(p_spam)
    prob_ham = math.exp(p_ham)
    print  '%30s' %j, '%10d' %y_true, '%10d' %y_pred, '%18.2f %%' % accuracy, '%10.6f'%prob_spam, '%10.6f'%prob_ham

print 'See confusion matrix. Top Left is predicted correctly as spam. Bottom right predicted correctly as ham:'
print conf_matrix
print 'Error rate: %4.2f'%(100-accuracy),'%%'