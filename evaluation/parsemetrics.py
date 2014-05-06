import os
import fnmatch
import sys

rootdir = './'
matches = []
for root, dirnames, filenames in os.walk(rootdir):
  for filename in fnmatch.filter(filenames, '*.snip'):
    path = os.path.join(root, filename)
    with open (path, 'r') as benchfile:
    content = inf.read()
    lines = content.split('\n')
    newLines = ''
    firstline = True
    metricscount = 0
    templine = ''
    for line in lines:
        if(firstline):
            newLines += line + '\n'
            firstline = False
            metricscount = line.count('\t')
            continue
        if(line == ''):
            continue
        currentcount = line.count('\t')
        if(currentcount < metricscount):
            if(templine != ''):
                tempcount = templine.count('\t')
                line = line[line.index('\t'):]
                if(tempcount + currentcount == metricscount):
                    newLines += templine + line + '\n'
                    templine = ''
                elif(tempcount + currentcount == metricscount+1):
                    newCount = int(float(templine[templine.rfind('\t')+1:]))
                    countIndex = line.find('\t')+1
                    countIndex2 = line.find('\t', countIndex)
                    oldCount = line[countIndex:countIndex2]
                    if(oldCount == ''):
                        oldCount = int(0)
                    else:
                        oldCount = int(float(oldCount))
                    newLines += templine[0:templine.rfind('\t')+1] + str(newCount + oldCount) + line[countIndex2:] + '\n'
                    templine = ''
            else:
                templine = line
        elif(currentcount == metricscount):
            newLines += line + '\n'
            templine = ''

    with open(path + '.parsed', 'w+') as newfile:
        newfile.write(newLines)
