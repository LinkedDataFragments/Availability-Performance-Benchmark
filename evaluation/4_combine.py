import os
import fnmatch
import sys

rootdir = './'
firstline = ''
with open('out.csv', 'w+') as outf:
  for root, dirnames, filenames in os.walk(rootdir):
    for filename in fnmatch.filter(filenames, '*.outy'):
      path = os.path.join(root, filename)
      with open(path) as thisfile:
        content = thisfile.readlines()
        if(firstline == ''):
          firsline = content[0]
          outf.write(firstline)
        content.pop(0)
        outf.write(''.join(content))
