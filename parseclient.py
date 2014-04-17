import sys
import csv
from collections import OrderedDict
from glob import glob

files = glob(sys.argv[1])

for path in files:

    outpath = path + '.out'

    values = {}
    perTimeStamp = {}
    with open(path, 'rb') as inf:
        has_header = csv.Sniffer().has_header(inf.read(1024))
        inf.seek(0)
        incsv = csv.DictReader(inf)
        if has_header:
            next(incsv)  # skip header row
        
        for row in incsv:
            values[row['label']] = row['label']
            if(row['timeStamp'] in perTimeStamp):
                perTimeStamp[row['timeStamp']][row['label']] = row['elapsed']
            else:
                perTimeStamp[row['timeStamp']] = {}
                perTimeStamp[row['timeStamp']][row['label']] = row['elapsed']

    with open(outpath, 'w') as outf:
        outf.write('timestamp\t' + '\t'.join(values) + '\n')

    perTimeStamp = OrderedDict(sorted(perTimeStamp.items(), key=lambda t: t[0]))

    with open(outpath, 'a') as outf:
        for key in perTimeStamp:
            rowValue = ''
            for value in values:
                rowValue = rowValue + '\t'
                if value in perTimeStamp[key]:
                    daValue = perTimeStamp[key][value]
                    rowValue = rowValue + str(daValue)
            outf.write(key + rowValue + '\n')
    
    
