import sys
from time import sleep

path = sys.argv[1]

with open(path + '.stop', 'w+') as myfile:
    myfile.write('write')

    
