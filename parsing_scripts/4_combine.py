import os
import fnmatch
import sys

rootdir = './'
firstline = ''
with open('out.csv', 'w+') as outf:
  outf.write('benchmark,clients,machine,metric,timestamp,cpu:core=0,cpu:core=1,cpu:core=2,cpu:core=3,cpu:iowait,memory:used,memory:actualused,disks:readbytes,disks:writebytes,network:bytessent,network:bytesrecv,network:speed\n')
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
