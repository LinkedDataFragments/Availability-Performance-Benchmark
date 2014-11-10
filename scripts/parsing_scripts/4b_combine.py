import os
import fnmatch
import sys

rootdir = './'
firstline = ''
with open('runmetrics.csv', 'w+') as outf:
  outf.write('benchmark,clients,machine,metric,Total actual runtime,Number of warmup runs,min/max Querymix runtime,Number of query mix runs (without warmups),Total runtime (sum),CQET (geom.),QMpH,Number of clients,Scale factor,CQET,Seed\n')
  for root, dirnames, filenames in os.walk(rootdir):
    for filename in fnmatch.filter(filenames, '*.runmetrics'):
      path = os.path.join(root, filename)
      with open(path) as thisfile:
        content = thisfile.readlines()
        if(firstline == ''):
          firsline = content[0]
          outf.write(firstline)
        content.pop(0)
        outf.write(''.join(content))
