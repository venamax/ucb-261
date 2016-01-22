#!/usr/bin/python
## mapper.py
## Author: Alejandro J. Rojas
## Description: mapper code for HW1.5

import sys
import re



########## Collect user input  ###############
filename = sys.argv[1]


def word_preprocessor(s):                                  ### This function eliminates some 
    elim_array = [',',                                 ### expressions to reduce the size of
                 '&',                                  ### vocabulary
                 '"', 
                  '|', 
                  '?', 
                  '-', 
                  '!', 
                  '.',
                  '$',
                   '(',
                   '#',
                    ' ',
                    'ly',
                     's',
                     '%',
                     '_',
                     "'",
                     '*',
                     '+',
                     '/',
                     "\\",
                     '@',
                     ')',
                     '=',
                     '>' ,
                  '[',
                  ']',
                  '>>',
                  ';',
                  '::',
                  ':',
                      ]
    s = re.sub( r'\d','',s)
    for item in  elim_array:    
        s = s.replace(item,'')
        s = s.strip(item)

    return s

def main(filename):
    with open (filename, "r") as myfile:

        for line in myfile.readlines():
            record = line.strip()
            record = re.compile('\W+')
            record = re.split(r'\t+', line)                    ### Each email is a record with 4 components
                                                           ### 1) ID 2) Spam Truth 3) Subject 4) Content
            if len(record)==4:                                 ### Take only complete records

                for i in range (2,len(record)):                ### Starting from Subject to the Content               
                    bagofwords = re.split(" ",record[i])       ### Collect all words present on each email               
                    for word in bagofwords: 
                        word = word_preprocessor(word).strip()
                        if word !="":
                            print word,'\t',  1, '\t', record[0],'\t',record[1],'\t' ### print out each word tuple               
            
if __name__ == "__main__":
    main(filename)