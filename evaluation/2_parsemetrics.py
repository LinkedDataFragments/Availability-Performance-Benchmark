import os
import fnmatch
import sys

rootdir = './'
matches = []
for root, dirnames, filenames in os.walk(rootdir):
  for filename in fnmatch.filter(filenames, '*.snip'):
    path = os.path.join(root, filename)
    with open (path, 'r') as inf:
      content = inf.read()
      lines = content.split('\n')
      newLines = ''
      firstline = True
      metricscount = 0
      templine = ''
      for line in lines:
          if(firstline):
              newLines += line + '\n'
              firstline = False
              metricscount = line.count('\t')
              continue
          if(line == ''):
              continue
          currentcount = line.count('\t')
          if(currentcount < metricscount):
              if(templine != ''):
                  line = line[line.index('\t'):]
                  countIndex = line.find('\t')+1
                  if(templine.count('\t') + line[countIndex:].count('\t') == metricscount):
                    newLines += templine + line[countIndex:] + '\n'
                  else :
                    newLines += templine + '\t' + line[countIndex:] + '\n'
                  templine = ''
              else:
                  templine = line
          elif(currentcount == metricscount):
              newLines += line + '\n'
              templine = ''

      with open(path + '.parsed', 'w+') as newfile:
          newfile.write(newLines)
