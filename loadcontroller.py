import sched, time
import os
#import numpy as np
import random
import pandas as pd
import sys
import datetime

s = sched.scheduler(time.time, time.sleep)
def changeLoad(sc): 
    if(not load):
        os.system('kubectl get event -o json > events2.txt')
        now = datetime.datetime.now(datetime.timezone.utc)
        print("end: ")
        print(str(now))
        sys.exit()
    else:
        n = load.pop(0)
        print(len(load))
        os.system('kubectl scale --replicas=' + str(n) + ' deployment loadgenerator')
        s.enter(60, 1, changeLoad, (sc,))


load = pd.read_csv('load.csv')['visitStartTime']
load = load.tolist()
now = datetime.datetime.now(datetime.timezone.utc)
print("start: ")
print(str(now))
s.enter(1, 1, changeLoad, (s,))
s.run()

