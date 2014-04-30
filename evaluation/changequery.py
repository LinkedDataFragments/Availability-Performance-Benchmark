import sys

count = int(sys.argv[1])
total = 12
text = ""
myFile = "./bsbmtools-0.2/queries/explore/ignoreQueries.txt"

for x in range (1, total+1):
    if(x != count):
        text += str(x) + "\n"

#text containts all queries that shouldn't be processed
with open(myFile, 'w+') as w:
    w.write(text)
