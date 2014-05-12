import sys
import csv
import glob
import re

files = glob.glob('*.csv')

def part(string):
    return int(re.findall('\d+', string.split(',')[1])[0])

def part2(string):
    return string.split(',')[0]

for path in files:
    with open(path) as inf:
        lines = inf.read().split('\n')
        header = lines.pop(0);
        lines = [line for line in lines if line.strip()]
        lines = sorted(lines, key=part)
        lines = sorted(lines, key=part2)

        with open(path + '.sorted', 'w+') as outf:
            outf.write(header + '\n')
            outf.write('\n'.join(lines))

    
