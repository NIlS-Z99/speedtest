scp -P 41592 -r pi@192.168.0.4:/home/pi/speedtest_logs/*.csv "E:\Dokumente\speedtest\speedtest_logs"
py "E:\Dokumente\speedtest\general_speedtest_analyse.py" 0 1
