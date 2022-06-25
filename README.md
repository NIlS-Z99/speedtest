# Internet Speedtest Automation
This repository is somewhat of a tutorial. It delivers all scripts and informations necessary for an automated internet speedtest setup with the linux tool [speedtest-cli](https://www.speedtest.net/de/apps/cli). My contributions are result evaluation scripts and a recommendation of an easy to implement automation infrastructure. Disclaimer: This repository will also be used as my personal speedtest result backup.


## Automation Setup
I suggest to setup automated speedtest runs with log file output on a linux home server, which is online most of the time anyways. The server has to have enough available bandwith and storage capacity and should idealy be placed as close to the router network-wise. E.g.: I run my speedtest-cli automation on my Raspberry Pi home server, which is directy connected to one of the routers 1 GBit/s Ports.
I suggest to run the evaluation on your main work station, especially if your home server is not setup to offer a graphical interface.


## Remote Machine Setup

### Debian-based OS
Update your package information <code>sudo apt update</code><br>
Install speedtest-cli with <code>sudo apt install speedtest-cli</code>

Now you could use this speedtest tool from your terminal to generate csv log files like this:
```sh
speedtest-cli --csv-header > <Log_File_Path>
speedetst-cli --csv >> <Log_File_Path>
```
The first line creates a csv file with the speetest header and the second line appends to the same file
So once you created the file you should from then on only append to that file using second command.
<br>
But we want to execute our speedtests according to a time shedule.
For this we need to use a task sheduler like [cron](https://wiki.ubuntuusers.de/Cron/). 
Cron offers us to install user-based crontabs, which are files, that describe when to execute a certain task/command.
To install a crontab you need to run the command <code>crontab -e</code>. 
My crontab was installed with privileged rights by prefixing the command with sudo.
The website [Crontab Guru](https://crontab.guru/) can help you to create desired shedules. E.g. my configuration looks like this:
```crontab
 30  0,3,6,9,12,15,18,21  * * 1-4 sudo speedtest-cli --csv --secure >> /home/pi/speedtest_logs/speedtest_$(date +\%B-\%Y).csv
  0  2,5,8,11,14,17,20,23 * * 1-4 sudo speedtest-cli --csv --secure >> /home/pi/speedtest_logs/speedtest_$(date +\%B-\%Y).csv
  5  0  1  *   *  sudo speedtest-cli --csv-header > /home/pi/speedtest_logs/speedtest_$(date +\%B-\%Y).csv
 10  0  1  *   *  sudo chown pi:root /home/pi/speedtest_logs/speedtest_$(date +\%B-\%Y).csv
 12  0  1  *   *  sudo chmod 666 /home/pi/speedtest_logs/speedtest_$(date +\%B-\%Y).csv
```


## Evaluation Machine Setup

### Windows

You should create a batch script like this:

```bat
scp -P <SSH_Reachable_Port> -r <USER>@<IP_ADRESS>:<speedtest_log_file_PATH_on_remote_machine>/*.csv <speedtest_log_file_folder_PATH_on_eva_machine> 
python <SCRIPT_FOLDER_PATH>\general_speedtest_analyse.py 0 1
```

Then you create a shortcut to this bat script and put it under <code>"C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"</code>
