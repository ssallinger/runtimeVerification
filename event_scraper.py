import os
import numpy as np
import sched, time

import datetime


s = sched.scheduler(time.time, time.sleep)
def getEvents(sc): 
    name = file_name.pop(0)
    os.system('kubectl get event -o json > events' + name + '.txt')
    
    now = datetime.datetime.now(datetime.timezone.utc)
    print('file events'  + name + '.txt saved at')
    print(str(now))

    s.enter(1800, 1, getEvents, (sc,))
    
file_name = ['1', '2', '3', '4', '5', '6']

s.enter(1, 1, getEvents, (s,))
s.run()



