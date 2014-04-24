import sys
from glob import glob
import re

files = glob('output/out_*')

for path in files:

    outpath = path + '.out'

    vb = 'Metrics for Query:      1\
Count:                  256 times executed in whole run\
AQET:                   0.006403 seconds (arithmetic mean)\
AQET(geom.):            0.006140 seconds (geometric mean)\
QPS:                    593.01 Queries per second\
minQET/maxQET:          0.00397338s / 0.02531122s\
Average result count:   0.00\
min/max result count:   0 / 0\
Number of timeouts:     0'

    allValues = {}
    resultList = []
    with open(path, 'r') as inf:
        content = inf.read()
        matches = re.findall('Metrics for Query:[\s\S]*?Number of timeouts:\s+\d+\n', content)
        for match in matches:
            resultValue = {}
            lines = match.split('\n')
            for line in lines:
                if(line != ''):
                    duo = line.split(':')
                    allValues[duo[0]] = duo[0]
                    resultValue[duo[0]] = re.findall('^[\d\s\./s]*', duo[1].strip())[0].strip()

            resultList.append(resultValue)
                    
            

    with open(outpath, 'w') as outf:
        outf.write('\t'.join(allValues) + '\n')

    with open(outpath, 'a') as outf:
        for result in resultList:                
            rowValue = ''
            for value in allValues:
                if value in result:
                    rowValue = rowValue + result[value]
                rowValue = rowValue + '\t'
            outf.write(rowValue + '\n')
        
