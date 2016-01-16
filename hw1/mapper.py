#!/usr/bin/python
## mapper.py
## Author: Alejandro J. Rojas
## Description: mapper code for HW1.3

import sys
import re



########## Collect user input  ###############
filename = sys.argv[1]
findwords = re.split(" ",sys.argv[2].lower())




with open (filename, "r") as myfile:

    for line in myfile.readlines():
        record = re.split(r'\t+', line)                    ### Each email is a record with 4 components
                                                           ### 1) ID 2) Spam Truth 3) Subject 4) Content
        if len(record)==4:                                 ### Take only complete records

            ########## Variables to collect and measure #########
            records = 0                                    ### Each record corresponds to a unique email
            words = 0                                      ### Words written in all emails incluidng Subject 
            spam_records, spam_words, spam_count = 0,0,0   ### Spam email count, words in spam email, user-specified word count
            ham_records, ham_words, ham_count = 0, 0, 0    ### Same as above but for not spam emails


            records += 1                                   ### add one the the total sum of emails
            if int(record[1]) == 1:                        ### If the email is labeled as spam
                spam_records += 1                          ### add one to the email spam count
                for i in range (2,len(record)):            ### Starting from Subject to the Content               
                    bagofwords = re.split(" ",record[i])   ### Collect all words present on each email                
                    for word in bagofwords:                ### For each word
                        words += 1                         ### add one to the total sum of words
                        spam_words += 1                    ### add one to the total sum of spam words  
                        for keyword in findwords:          ### for each word specified by user
                            if keyword in word:            ### If there's a match then
                                spam_count += 1            ### add one to the user specified word count as spam
                                
            else:                                          ### If email is not labeled as spam
                ham_records +=1                            ### add one to the email ham count
                for i in range (2,len(record)):            ### Starting from Subject to the Content               
                    bagofwords = re.split(" ",record[i])   ### Collect all words present on each email                
                    for word in bagofwords:                ### For each word
                        words += 1                         ### add one to the total sum of words
                        ham_words += 1                     ### add one to the total sum of ham words  
                        for keyword in findwords:          ### for each word specified by user
                            if keyword in word:            ### If there's a match then
                                ham_count += 1             ### add one to the user specified word count as ham
                    

            print spam_count, " ", spam_words, " ", spam_records, " ", ham_count, " ", ham_words, " ", ham_records, " ", words, " ", records, " ",record[0], " ", record[1]