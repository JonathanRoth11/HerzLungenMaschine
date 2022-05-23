# Import external packages

from multiprocessing.connection import wait
import pandas as pd
from datetime import datetime
import numpy as np
import re

# Classes 

class Subject():
    def __init__(self, file_name):

        ### Aufgabe 1: Interpolation ###

        __f = open(file_name)
        self.subject_data = pd.read_csv(__f)
        self.subject_data = self.subject_data.interpolate(method = 'spline', axis=0, order = 1)
        #__splited_id = re.findall(r'\d+',file_name)      
        self.subject_id = file_name.split('.csv')[0][-1]
        self.names = self.subject_data.columns.values.tolist()
        self.time = self.subject_data["Time (s)"]        
        self.spO2 = self.subject_data["SpO2 (%)"]
        self.temp = self.subject_data["Temp (C)"]
        self.blood_flow = self.subject_data["Blood Flow (ml/s)"]
        print('Subject ' + self.subject_id + ' initialized')

### Aufgabe 2: Datenverarbeitung ###

def calculate_CMA(df,n):
    return df.expanding(n).mean()
    

def calculate_SMA(df,n):
    return df.rolling(n).mean()

###Aufgabe 3
# def mehrals(flow, min, max):
    
#     time_start_max = null
#     time_start_min = null 
#     timeuplimit = 0
#     timelowlimit = 0

#     for x in flow:
        
#         if x.loc['Blood Flow (ml/s)'] > max:

#             if time_start_max is not null: 
#                 if x.loc['Time (s)'] - time_start_max >=3 :
#                     timeuplimit = timeuplimit + ( x.loc['Time (s)'] - bevor_time)
#                 else:
#                     time_start_max = time_start_max
#             else:
#                 time_start_max = x.loc['Time (s)']

#         else :
#             time_start_max = null 

#         if x.loc['Blood Flow (ml/s)'] <= min:

#             if time_start_min is not null: 
#                 if x.loc['Time (s)'] - time_start_min >=3 :
#                     timelowlimit = timelowlimit + ( x.loc['Time (s)'] - bevor_time)
#                 else:
#                     time_start_min = time_start_min
#             else:
#                 time_start_min = x.loc['Time (s)']

#         else :
#             time_start_min = null 

#         bevor_time = x.loc['Time (s)']

#     return timelowlimit + timeuplimit 
        


### Aufgabe 4 
#4.1 
# Simple Moving Average ist sinnvoll für Signale die eher glatte Ablauf haben sollten - in Wirklichkeit kann es nicht dazu vorkommen, 
# dass das Unterschied zwischen den Werten schnell und um hoch sich ändert, sowie für Signale, welche potenzial, 
# von aussen leicht gestört sein könnten, was resultiert mit einem unrealistischen Peak auf dem Diagramm.

# 4.2 
# Je grösser n ist, desto Funktionsablauf ist glatter. Die Werte sind stark beeinflusst.
