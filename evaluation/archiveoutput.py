import json
import glob
import os
import time
import datetime
import socket

with open('./eval.options') as content_file:
    content = content_file.read()

options = json.loads(content)

ts = time.time()
newdir = options['outputfolder'] + socket.gethostname() + '_' + options['tester'] + '_' + str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')) + '/'
os.mkdir(newdir)

files = glob.glob(options['outputfolder'] + "*")

for file in files:
    if(os.path.isfile(file)):
        os.rename(file, newdir + os.path.basename(file))
