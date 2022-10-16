from threading import Thread
import time

print('ddddddddddddddddddd')

def clock_for():
    ko_nowtime = time.strftime('%H-%M', time.localtime(time.time()))
    return ko_nowtime

alarms = [
        {'id': 1, 'hour': 16, 'minute': 51, 'missionType' : '랜덤'},
        {'id': 2, 'hour': 7, 'minute': 00, 'missionType' : '사진 매칭'}
        ]

def ringing_alarm():
    print('띠로리') 

def when_toAlarm():
    for alarm in alarms:
        if f'{alarm["hour"]}-{alarm["minute"]}' == str(clock_for()):
            ringing_alarm() 

proc = Thread(target=when_toAlarm, args=())
proc2 = Thread(target=clock_for, args=())
proc.start()
proc2.start()