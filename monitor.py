import os
import numpy as np
import sched, time
import json
import datetime
import pandas as pd

#trace = pd.DataFrame(columns = ['uid','time', 'name', 'podType', 'event'])

trace_dict = {}


def buildMatrix(trace):
    matrix = pd.DataFrame(columns = ['time', 'nrLoadgenerators', 'nrFrontends'])
    stepSize = datetime.timedelta(seconds=10)
    # sort trace by time
    trace.sort_values(by=['time'], inplace=True)
    # assumption: starting from 0,0 config
    # first row: all 0, then increment gradually 
    firstTs = trace['time'].iloc[0]
    lastTs = trace['time'].iloc[-1]
    
    currentTime = firstTs - stepSize
    nrFrontends = 0
    nrLoadgenerators = 0
    matrix = matrix.append(pd.Series([currentTime, nrLoadgenerators, nrFrontends], index=matrix.columns), ignore_index=True)
    idx = 0


    # walk over trace + evaluate change at every step
    while(currentTime <= lastTs + stepSize):
        while(idx < len(trace) and trace['time'].iloc[idx] <= currentTime):
            if(trace['podType'].iloc[idx] == 'frontend' and trace['event'].iloc[idx] == 'Killing'):
                nrFrontends = nrFrontends - 1
            if(trace['podType'].iloc[idx] == 'frontend' and trace['event'].iloc[idx] == 'Created'):
                nrFrontends = nrFrontends + 1
            if(trace['podType'].iloc[idx] == 'loadgenerator' and trace['event'].iloc[idx] == 'Killing'):
                nrLoadgenerators = nrLoadgenerators - 1
            if(trace['podType'].iloc[idx] == 'loadgenerator' and trace['event'].iloc[idx] == 'Created'):
                nrLoadgenerators = nrLoadgenerators + 1
            idx = idx + 1
        
        currentTime = currentTime + stepSize
        matrix = matrix.append(pd.Series([currentTime, nrLoadgenerators, nrFrontends], index=matrix.columns), ignore_index=True)

    print("matrix:")
    print(matrix.head(10))
    matrix.to_csv('matrix.csv')

s = sched.scheduler(time.time, time.sleep)
def getEvents(sc): 
    os.system('kubectl get event -o json > events1.txt')
    with open('events1.txt') as events_file:
        events = json.load(events_file)
        for e in events['items']:
            if(e['reason']=='Created' or e['reason']=='Killing'):
                #print(e['firstTimestamp'])
                #print(e['metadata']['name'])
                #print(e['reason'])
                time = datetime.datetime.strptime(e['firstTimestamp'], "%Y-%m-%dT%H:%M:%SZ")
                trace_dict[e['metadata']['uid']] = [time, e['metadata']['name'], e['metadata']['name'].partition('-')[0], e['reason']]
    
    trace = pd.DataFrame.from_dict(trace_dict, orient='index', columns = ['time', 'name', 'podType', 'event'])
    print('trace:')
    print(trace.head())
    trace.to_csv('trace.csv')
    #buildMatrix(trace)
    #print('done')
    s.enter(10, 1, getEvents, (sc,))
    

s.enter(1, 1, getEvents, (s,))
s.run()



