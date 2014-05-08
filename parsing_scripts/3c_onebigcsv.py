import os
import fnmatch
import sys

rootdir = './'
matches = []
for root, dirnames, filenames in os.walk(rootdir):
  for filename in fnmatch.filter(filenames, 'queryexecutiontimes.txt.*'):
    path = os.path.join(root, filename)
    parts = path.replace(rootdir, '').split(os.sep)
    if(filename.index(parts[3]) == 0):
      with open(path) as thisfile:
        content = thisfile.readlines()
        first = True
        newcontent = ''
        for line in content:
          if(first):
            line = 'benchmark\tclients\tmachine\tmetric\t' + line
            newcontent += line
            first = False
            continue
          line = parts[0] + '\t' + parts[1] + '\t' + parts[2] + '\t' + filename.split('.')[0] + '\t' + line
          newcontent += line
        with open(path + '.dbmetrics', 'w+') as outf:
          outf.write(newcontent.replace('\t', ','))
              
