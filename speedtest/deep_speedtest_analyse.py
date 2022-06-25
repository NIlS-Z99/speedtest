from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import sys


filename = "speedtest.csv"
if len(sys.argv)>1:
    filename = sys.argv[1]

def formatDateTime(x):
    return datetime.strptime(x,'%Y-%m-%dT%H:%M:%S.%fZ')

dataFrame = pd.read_csv(filename,header=0)
server_ids = set(dataFrame['Server ID'])
timestamps,legend = ([],[])
axes = [plt.figure(0).add_subplot(),plt.figure(1).add_subplot(),plt.figure(2).add_subplot()]
for server_id in server_ids:
    frame = dataFrame.loc[dataFrame['Server ID']==server_id,['Sponsor','Timestamp','Download','Upload','Ping']]
    timestamps.append(list(map(formatDateTime,frame['Timestamp'])))
    frame['Timestamp'] =  list(map(lambda x: x.day+float(x.hour)/100,timestamps[-1]))
    frame['Download'] =  list(map(lambda x: x/1000000,frame['Download']))
    frame['Upload'] =  list(map(lambda x: x/1000000,frame['Upload']))
    frame.index = frame.index//10
    axes[0].plot(frame['Timestamp'], frame['Download'])
    axes[1].plot(frame['Timestamp'], frame['Upload'])
    axes[2].plot(frame['Timestamp'], frame['Ping'])
    legend.append(frame['Sponsor'][0])
for idx in range(len(axes)):
    axes[idx].legend(legend)
    axes[idx].set_xlabel('Days.Hours')
    axes[idx].set_ylabel('MBit/s')
axes[2].set_ylabel('ms')
axes[0].set_title('Download')
axes[1].set_title('Upload')
axes[2].set_title('Ping')
plt.show()