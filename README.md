# Internet Speedtest Automation
This repository is somewhat of a tutorial. It delivers all scripts and informations necessary for an automated internet speedtest setup with the linux tool [speedtest-cli](https://www.speedtest.net/de/apps/cli). My contributions are result evaluation scripts and a recommendation of an easy to implement automation infrastructure. Disclaimer: This repository will also be used as my personal speedtest result backup.


## Automation Setup
I suggest to setup automated speedtest runs with log file output on a linux home server, which is online most of the time anyways. The server has to have enough available bandwith and storage capacity and should idealy be placed as close to the router network-wise. E.g.: I run my speedtest-cli automation on my Raspberry Pi home server, which is directy connected to one of the routers 1 GBit/s Ports.
I suggest to run the evaluation on your main work station, especially if your home server is not setup to offer a graphical interface.


## Remote Machine Setup

### Debian-based OS
Update your package information <code>sudo apt update</code><br>
Install speedtest-cli with <code>sudo apt install speedtest-cli</code>

Now you could use this speedtest tool from your terminal like this:
```sh
speedtest-cli 
```

But we want to execute our speedtests according to a time shedule.
For this we need to use a task sheduler like [cron](https://wiki.ubuntuusers.de/Cron/). 
Cron offers us to install user-based crontabs, which are files, that describe when to execute a certain task/command.
The website [Crontab Guru](https://crontab.guru/) can help you to create desired shedules. E.g. my configuration looks like this:
```crontab
speedtest-cli 
```


## Evaluation Machine Setup

### Windows

You should create a batch script like this:

```bat
scp -P <SSH_Reachable_Port> -r <username>@<IP_ADRESS>:<speedtest_log_file_PATH_on_remote_machine>/*.csv <speedtest_log_file_folder_PATH_on_eva_machine> 
python <PATH_to_the_script>\general_speedtest_analyse.py 0 1
```

Then you create a shortcut to this bat script and put it under <code>"C:\Users\<username>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs"</code>
