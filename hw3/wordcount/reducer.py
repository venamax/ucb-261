#!/usr/bin/python
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
initials = list(map(chr,range(97,123)))
wordcounts = {}
wordfrequencies = {}
sum_total=0

# input comes from STDIN


# input comes from STDIN
for line in sys.stdin:

    line = line.strip()                        ### remove leading and trailing whitespace
    line = line.split('\t')                    ### parse the input we got from mappe
    word = line[0]

    if line[0] == '*':
        sum_total += int(line[1])
    
    else:
    
        initial = str(word[0])
    
        if initial in initials:
            try:

                count = line[1]
                count = int(count)                      ### convert count (currently a string) to int
                if count > 100000:
                    sys.stderr.write("reporter:counter:CombinerCalls:,%s,1\n"%word)
                                         

            except ValueError:                          ### if count was not a number then silently                         
                continue                                ### ignore/discard this line

                                                
                                                
            if current_word == word:                     ### this IF-switch only works because Hadoop sorts map output
                current_count += count*1.0                  ### by key (here: number) before it is passed to the reducer
            else:
                if current_word:
          
                    wordcounts[current_word] = current_count
                    wordfrequencies[current_word] = current_count/sum_total
                current_count = count                    ### set current count
                current_word = word                      ### set current word


if current_word == word:                         ### do not forget to output the last word if needed!
    wordcounts[current_word] = current_count
    wordfrequencies[current_word]= current_count/sum_total

topwords = sorted(wordfrequencies, key=wordfrequencies.__getitem__, reverse = True) ## sort 
for i in range (len(topwords)):
    word = topwords[i]
    print '"%s"\t%s\t%s'%(word,wordcounts[word],wordfrequencies[word])
    sys.stderr.write("reporter:counter:ReducerCalls:,Calls,1\n")