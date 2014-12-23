#! /usr/bin/python

from subprocess import Popen,PIPE
from datetime import datetime
from time import sleep
import numpy as np

def getTemp():
    p = Popen(['/opt/vc/bin/vcgencmd','measure_temp'],stdout=PIPE)
    stdout = p.communicate()
    tmp = float(stdout[0].split('=')[1].split('\'')[0])

    #p = Popen(['cat','/sys/class/thermal/thermal_zone0/temp'],stdout=PIPE)
    #tmp = float(p.communicate()[0])/1000.0
    
    return tmp

with open('static/temps.tsv','w') as f:
    f.write('date\tclose\n')

n = 20
W = np.array(range(0,n))
W = np.exp(-0.16*W)
W /= np.sum(W)
temps = [getTemp()]*int(n)
while True:
    with open('static/temps.tsv','a') as f:
        date_str = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        f.write('%s\t%f\n'%(date_str, np.sum(np.array(temps)*W)))

    temps.append( getTemp() )
    temps = temps[1:]
    sleep(60);


