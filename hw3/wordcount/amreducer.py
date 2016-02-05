#!/usr/bin/python
from operator import itemgetter
import sys

current_word = None
current_count = 0
word = None
initials = list(map(chr,range(97,110)))
words = {}

# input comes from STDIN


# input comes from STDIN
for line in sys.stdin:

    line = line.strip()                        ### remove leading and trailing whitespace
    line = line.split('\t')                    ### parse the input we got from mappe
    word = line[0]
    initial = str(word[0])
    
    if initial in initials:
        try:

            count = line[1]
            count = int(count)                      ### convert count (currently a string) to int
        except ValueError:                          ### if count was not a number then silently                         
            continue                                ### ignore/discard this line

                                                
                                                
        if current_word == word:                     ### this IF-switch only works because Hadoop sorts map output
            current_count += count                  ### by key (here: number) before it is passed to the reducer
        else:
            if current_word:
          
                words[current_word] = current_count  ### store tuple in a list once totalize count per number
  
            current_count = count                    ### set current count
            current_word = word                      ### set current word


if current_word == word:                         ### do not forget to output the last word if needed!
    words[current_word] = current_count 

for word in words:
    print 'We found "%s"' %word, ' on %s'%words[word] , 'occassions.'
    sys.stderr.write("reporter:counter:ReducerCalls:,Calls,1\n")