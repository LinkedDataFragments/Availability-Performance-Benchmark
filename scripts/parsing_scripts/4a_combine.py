#!/usr/bin/env python
import os
import fnmatch
import sys

rootdir = './'
firstline = ''
with open('outmetrics.csv', 'w+') as outf:
  outf.write('benchmark,clients,machine,metric,Count,Average result (Bytes),min/max result (Bytes),AQET(geom.),Number of timeouts,AQET,minQET/maxQET,Average result count,Metrics for Query,QPS,min/max result count\n')
  for root, dirnames, filenames in os.walk(rootdir):
    for filename in fnmatch.filter(filenames, '*.outmetrics'):
      path = os.path.join(root, filename)
      with open(path) as thisfile:
        content = thisfile.readlines()
        if(firstline == ''):
          firsline = content[0]
          outf.write(firstline)
        content.pop(0)
        outf.write(''.join(content))
