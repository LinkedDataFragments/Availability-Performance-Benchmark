#!/usr/bin/env python
import os
import fnmatch
import sys

rootdir = './'
firstline = ''
with open('dbmetrics.csv', 'w+') as outf:
  outf.write('benchmark,clients,machine,metric,QueryID,Total Execution Time,Avg Execution Time,Number of Queries per Hour\n')
  for root, dirnames, filenames in os.walk(rootdir):
    for filename in fnmatch.filter(filenames, '*.dbmetrics'):
      path = os.path.join(root, filename)
      with open(path) as thisfile:
        content = thisfile.readlines()
        if(firstline == ''):
          firsline = content[0]
          outf.write(firstline)
        content.pop(0)
        outf.write(''.join(content))
