#!/usr/bin/env python
import os
import fnmatch
import sys
import re

rootdir = './'
matches = []

for root, dirnames, filenames in os.walk(rootdir):
  for filename in fnmatch.filter(filenames, 'out_1.txt'):
    path = os.path.join(root, filename)
    allValues = {}
    resultList = []
    with open (path, 'r') as inf:
        content = inf.read()
        matches = re.findall('Scale factor:[\s\S]*?CQET \(geom.\):[^\n]+?\n', content)
        for match in matches:
            resultValue = {}
            lines = match.split('\n')
            for line in lines:
                if(line != ''):
                    duo = line.split(':')
                    allValues[duo[0]] = duo[0]
                    resultValue[duo[0]] = re.findall('^[\d\s\./s]*', duo[1].strip())[0].strip()

            resultList.append(resultValue)
                    
            

    with open(path + '.run', 'w+') as outf:
        outf.write('\t'.join(allValues) + '\n')

    with open(path + '.run', 'a') as outf:
        for result in resultList:                
            rowValue = ''
            for value in allValues:
                if value in result:
                    rowValue = rowValue + result[value]
                rowValue = rowValue + '\t'
            outf.write(rowValue + '\n')
        
