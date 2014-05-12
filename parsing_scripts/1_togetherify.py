import os
import fnmatch
import glob
import sys
import re

rootdir = './'
matches = []
for root, dirnames, filenames in os.walk(rootdir):
  for filename in fnmatch.filter(filenames, '*.csv'):
    path = os.path.join(root, filename)
    parts = path.replace(rootdir, '').split(os.sep)
    if(len(parts) >= 2):
      tpath = glob.glob(rootdir + '/' + parts[0] + '/' + parts[1] + '/*/timing.txt')
      with open(tpath[0], 'r') as timingfile:
          content = timingfile.read()
          m = re.search('---Starting benchmark[\s\S]*?(\d{13})[\s\S]*?---Stopping benchmark[\s\S]*?(\d{13})[\s\S]*?$', content)
          timing1 = int(m.group(1))
          timing2 = int(m.group(2))
      with open (path, 'r') as benchfile:
          content = benchfile.read()
          lines = content.split('\n')
          newLines = ''
          firstline = True
          for line in lines:
              if(firstline):
                  newLines += line + '\n'
                  firstline = False
                  continue
              if(line == ''):
                  continue
              temp = str(line.split('\t')[0])
              timestamp = int(float(temp))
              if(timing1 < timestamp & timestamp < timing2):
                  newLines+= line + '\n'

          with open (path + '.snip', 'w+') as newfile:
              newfile.write(newLines)

              
          
      

