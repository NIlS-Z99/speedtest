from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from glob import glob
from numpy.lib.function_base import append
import pandas as pd
import sys,os,math

def formatDateTime(x):
    return datetime.strptime(x,'%Y-%m-%dT%H:%M:%S.%fZ')
MAX_DOWN = 120
MAX_UP = 20
NO_SHOW = False
SAVE_FILE = False

os.system('color')
filenames = glob(os.path.join(os.path.dirname(os.path.abspath(__file__)),"speedtest_logs","*.csv"))
if len(sys.argv)>1 and int(sys.argv[1])>0:
    NO_SHOW = True
if len(sys.argv)>2 and int(sys.argv[2])>0:
    SAVE_FILE = True
if len(sys.argv)>3:
    filenames = sys.argv[3:]


results = ""
output = "Speedtest Statistics\n--------------------"
for filename in filenames:
    dataFrame = pd.read_csv(filename,header=0)
    timestamps = list(map(formatDateTime,dataFrame['Timestamp']))
    dataFrame['Timestamp'] = list(map(lambda x: x.day+float(x.hour)/100,timestamps))
    dataFrame['Download'] = list(map(lambda x: x/1000000,dataFrame['Download']))
    dataFrame['Upload'] = list(map(lambda x: x/1000000,dataFrame['Upload']))
    ref = list(set(dataFrame['Sponsor']))

    if len(dataFrame['Timestamp'])>0:
        print("\n")
        print("Timestamp:   Download  |   Upload   |   Ping   -> SpeedTest-Server")
        print("------------------------------------------------------------------")
        quintiles = list(zip(dataFrame['Sponsor'],dataFrame['Timestamp'],dataFrame['Download'],dataFrame['Upload'],dataFrame['Ping']))
        for idx,quintile in enumerate(quintiles): 
            print("[{:2}d {:2}h]: {:6.2f} MB/s | {:5.2f} MB/s | {:5.2f} ms -> {}".format(
                int(quintile[1]),int((quintile[1]*100)%100),quintile[2],quintile[3],quintile[4],quintile[0]))
        res_stats = "                     min     |     avg      |     max\n"+ \
                    "                -------------|--------------|--------------\n"+ \
                    "Download-Speed: {:7.3f} MB/s | {:7.3f} MB/s | {:7.3f} MB/s\n".format(round(min(dataFrame["Download"]),3),round(sum(dataFrame["Download"])/len(dataFrame["Download"]),3),round(max(dataFrame["Download"]),3))+ \
                    "  Upload-Speed: {:7.3f} MB/s | {:7.3f} MB/s | {:7.3f} MB/s\n".format(round(min(dataFrame["Upload"]),3),round(sum(dataFrame["Upload"])/len(dataFrame["Upload"]),3),round(max(dataFrame["Upload"]),3))+ \
                    "          Ping: {:7.3f} ms   | {:7.3f} ms   | {:7.3f} ms\n\n".format(round(min(dataFrame["Ping"]),3),round(sum(dataFrame["Ping"])/len(dataFrame["Ping"]),3),round(max(dataFrame["Ping"]),3))
        print("\n"+res_stats)
        output += "\n\nResults for "+filename.split('_')[-1].split('-')[0]+":\n\n"+res_stats
        insufficent_down,insufficent_up = ([],[])
        for down_speed,up_speed in zip(dataFrame["Download"],dataFrame["Upload"]):
            if(math.ceil(down_speed)<MAX_DOWN*0.9): insufficent_down.append(down_speed)
            if(math.ceil(up_speed)<MAX_UP*0.9): insufficent_down.append(down_speed)
        download = str(str('\033[91m'+"Insufficent") if(len(insufficent_down)>int(round(0.1*len(dataFrame["Download"])))) else str('\033[92m'+"Sufficent"))+" Download Speed Consistency"+'\033[0m'
        upload = str(str('\033[91m'+"Insufficent") if(len(insufficent_up)>int(round(0.1*len(dataFrame["Upload"])))) else str('\033[92m'+"Sufficent"))+" Upload Speed Consistency"+'\033[0m'
        output += ("Insufficent" if "Insufficent" in download else "Sufficent") + " Download Speed Consistency\n"
        output += ("Insufficent" if "Insufficent" in upload else "Sufficent") + " Upload Speed Consistency\n\n"
        results+="\n\n"+filename.split('_')[-1].split('-')[0]+"\n" 
        results+=download+"\n"+upload
        print(download+"\n"+upload+"\n\n") 


        index = [*range(len(timestamps))]
        xticks = list(map(lambda timestamp: str(timestamp.day)+"d\n"+str(timestamp.hour)+"h", timestamps))
        legend = ['Download','Upload','Ping']
        sponsorLabels = [Line2D([0], [0], lw=1, label=str(str(idx)+" "+label)) for idx,label in enumerate(ref)]


        for it in range(int(len(dataFrame['Timestamp'])/30)):
            begin = it*30
            end = (it+1)*30
            
            fig = plt.figure()  
            plt.tick_params(axis='both',which='both',bottom=False,left=False,labelleft=False,labelbottom=False) 
            ax1 = fig.add_subplot()
            ax2 = ax1.twinx()

            for idx,quintile in zip([*range(begin,end)],quintiles[begin:end]): 
                ax1.annotate(ref.index(quintile[0]),xy=(idx,quintile[3]),xycoords='data',xytext=(idx-0.1, quintile[3]+2), textcoords='data')

            ax1.set_ylabel('MBit/s',color='tab:cyan')
            ax1.tick_params(axis='y',labelcolor='tab:cyan')
            ax1.scatter(index[begin:end], dataFrame[begin:end][legend[0]], color='tab:blue')
            down, = ax1.plot(index[begin:end], dataFrame[begin:end][legend[0]], color='tab:blue', label=legend[0])
            ax1.scatter(index[begin:end], dataFrame[begin:end][legend[1]], color='tab:green')
            up, = ax1.plot(index[begin:end], dataFrame[begin:end][legend[1]], color='tab:green', label=legend[1])
            ax2.set_ylabel('Ping in ms',color='tab:red')
            ax2.tick_params(axis='y',labelcolor='tab:red')
            ax2.scatter(index[begin:end], dataFrame[begin:end][legend[2]], color='tab:red')
            ping, = ax2.plot(index[begin:end], dataFrame[begin:end][legend[2]], color='tab:red', label=legend[2])

            plt.xticks(ticks=index[begin:end],labels=xticks[begin:end])
            plt.title('Speedtest Results '+filename.split('_')[-1].split('-')[0]+'#'+str(it))
            plt.legend(handles=[down,up,ping,*sponsorLabels], loc='upper center', bbox_to_anchor=(0.5, -0.075), fancybox=True, shadow=True, ncol=4)
            plt.subplots_adjust(top=0.975,bottom=0.335)
            fig.set_size_inches(14, 8.5)
            plt.savefig(str('plots/Speedtest Results '+filename.split('_')[-1].split('-')[0]+'#'+str(it)+".png"))

        if NO_SHOW: 
            plt.clf()
            plt.cla()
            plt.close('all')
        else: plt.show()
            

print("\n\nSummary\n--------",results,"\n")
if SAVE_FILE: 
    with open("speedtest_res.txt","w") as res_file: res_file.write(output)
input("Press Enter to Close!")
