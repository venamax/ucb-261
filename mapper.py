#!/usr/bin/python
import sys
import re
count = 0
WORD_RE = re.compile(r"[\w']+")
filename = sys.argv[2]
findword = sys.argv[1]
with open (filename, "r") as myfile:
#Please insert your code
    for line in myfile.readlines():
        if findword.lower() in line: 
            count = count + 1
        elif findword.upper() in line:
            count = count + 1
        elif findword.capitalize() in line:
            count = count + 1
print count