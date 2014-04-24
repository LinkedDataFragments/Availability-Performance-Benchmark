import telnetlib
import time
import sys
import os.path
import threading        

output = './' + sys.argv[1]
metric = sys.argv[2].replace('--', '\t')
host = sys.argv[3]

if os.path.isfile(output + ".stop"):
    os.remove(output + ".stop")

with open(output, "w") as myfile:
    myfile.write('timestamp\t' + metric + '\n')
    
print 'started'

telnet = telnetlib.Telnet(host, 4444)
telnet.write('test\n')
telnet.read_until('\n')
telnet.write('metrics:' + metric + '\n')
while not os.path.isfile(output + '.stop'):
    value = telnet.read_until('\n', 1).strip()
    if(value != ''):
        with open(output, "a") as myfile:
            myfile.write(str(time.time()*1000) + '\t' + value + '\n')

telnet.write('exit\n')
print telnet.read_all()
