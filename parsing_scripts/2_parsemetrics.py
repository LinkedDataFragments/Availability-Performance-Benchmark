import os
import fnmatch
import sys

rootdir = './'
matches = []
lines_seen = set() # holds lines already seen
current_timestamp = 0
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
          if line in lines_seen:
              continue
          lines_seen.add(line)
          if(firstline):
              newLines += line + '\n'
              firstline = False
              metricscount = line.count('\t')
              continue
          if(line == ''):
              continue
          this_timestamp = int(line[2:13])
          if()
          if(line.rfind('\t-1') == -1):
            templine = line
          else:
            if(templine != ''):
              line = line[line.index('\t'):]
              countIndex = line.find('\t')+1
              if(templine.count('\t') + line[countIndex:].count('\t') == metricscount):
                line = templine + line[countIndex:]
                if line in lines_seen:
                  continue
                lines_seen.add(line)
                newLines += line + '\n'
              else :
                line = templine + '\t' + line[countIndex:]
                if line in lines_seen:
                  continue
                lines_seen.add(line)
                newLines += line + '\n'
                templine = ''
            else:
              newLines += line + '\n'
##          currentcount = line.count('\t')
##          if(currentcount < metricscount):
##              if(templine != ''):
##                  line = line[line.index('\t'):]
##                  countIndex = line.find('\t')+1
##                  if(templine.count('\t') + line[countIndex:].count('\t') == metricscount):
##                    newLines += templine + line[countIndex:] + '\n'
##                  else :
##                    newLines += templine + '\t' + line[countIndex:] + '\n'
##                  templine = ''
##              else:
##                  templine = line
##          elif(currentcount == metricscount):
##              newLines += line + '\n'
##              templine = ''

      with open(path + '.parsed', 'w+') as newfile:
          newfile.write(newLines)
