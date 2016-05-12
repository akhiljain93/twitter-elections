import os
f = open('urls.txt', 'r')
for line in f:
    line=line.strip()
    cmd = "python selenium_parse.py " + line + " > data/" + line + " &" 
    print cmd
    os.system(cmd)
