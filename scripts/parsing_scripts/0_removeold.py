import os
import fnmatch
import sys

rootdir = './'
firstline = ''
for root, dirnames, filenames in os.walk(rootdir):
  for filename in fnmatch.filter(filenames, '*.outy'):
    path = os.path.join(root, filename)
    os.remove(path)
  for filename in fnmatch.filter(filenames, '*.parsed'):
    path = os.path.join(root, filename)
    os.remove(path)
  for filename in fnmatch.filter(filenames, '*.snip'):
    path = os.path.join(root, filename)
    os.remove(path)
os.remove('out.csv')
os.remove('outmetrics.csv')
