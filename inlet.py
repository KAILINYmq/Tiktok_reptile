import os,time

while True:
    time_now = time.strftime("%H:%M", time.localtime())
    if time_now in ["08:30", "13:00", "23:30"]:
        os.system('python ./main.py')
        time.sleep(3900)