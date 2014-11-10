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
      current_timestamp = 0
      lines = content.split('\n')
      newLines = ''
      firstline = True
      metricscount = 0
      current_line = ''
      current_finished = False
      for line in lines:
          if(firstline):
              newLines += line + '\n'
              firstline = False
              metricscount = line.count('\t')
              continue
          if(line == ''):
              continue
          this_timestamp = int(float(line[0:line.find('\t')])) #get current timestamp
          if(this_timestamp > current_timestamp+500):
            current_finished = False
            current_line = ''
          if(current_finished == True):
            continue
          
          if(line.rfind('\t-1') == -1): #incomplete 
            current_line = line
          else:
            if(current_line != ''): # busy with incomplete
              if current_line[current_line.find('\t'):] in line:
                newLines += line + '\n'
              else:
                line = line[line.index('\t'):]
                countIndex = line.find('\t')+1
                if(current_line.count('\t') + line[countIndex:].count('\t') == metricscount):
                  line = current_line + line[countIndex:]
                  newLines += line + '\n'
                else :
                  line = current_line + '\t' + line[countIndex:]
                  newLines += line + '\n'
            else:
              newLines += line + '\n'
            current_finished = True
          current_timestamp = this_timestamp

      with open(path + '.parsed', 'w+') as newfile:
        lines = newLines.split('\n')
        for line in lines:
          if(line.count('\t') == metricscount):
            newfile.write(line + '\n')
