#! /usr/bin/python

import sys
from subprocess import Popen,PIPE
from datetime import datetime
from time import sleep
import MySQLdb as mdb

def getTemp():
    p = Popen(['/opt/vc/bin/vcgencmd','measure_temp'],stdout=PIPE)
    stdout = p.communicate()
    tmp = float(stdout[0].split('=')[1].split('\'')[0])

    #p = Popen(['cat','/sys/class/thermal/thermal_zone0/temp'],stdout=PIPE)
    #tmp = float(p.communicate()[0])/1000.0
    
    return tmp

with open('static/temps.tsv','w') as f:
    f.write('date\tclose\n')

logging_int = 60. # once a minute
if len(sys.argv)>1:
    logging_int = float(sys.argv[1])

while True:
    try:
        with mdb.connect('localhost','root','raspberry','temps') as con:
            date_str = datetime.now().strftime('%y-%m-%d %H:%M:%S')
            sql = "INSERT INTO tblTemps VALUES ('%s',%f);"%(date_str,getTemp())
            con.execute(sql)
    except mdb.Error, e:
        print('MySQL Error %d: %s'%(e.args[0],e.args[1]))

    sleep(logging_int);


