from operator import is_
import threading
from flask import Flask, request, redirect
from threading import Thread
#import RPi as GPIO #디버깅 하려고 일단 주석처리
import time
import RPi.GPIO as GPIO
import cv2
import numpy as np
import time
import random
import Adafruit_SSD1306
import _functions.alarmpi as buz
from PIL import Image, ImageDraw, ImageFont
import _functions.calculate as calcul_mission
import _functions.card_detection as card_mission
import _functions.reaction_speed_test as reaction_mission
from multiprocessing import Process

GPIO.setwarnings(False)

button_red = 9
button_yellow =  10
button_blue = 11

piezzo_buzzer = 15

led = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(button_red, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button_yellow, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(button_blue, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(piezzo_buzzer, GPIO.OUT)
GPIO.setup(led, GPIO.OUT)




app = Flask(__name__)

### data ##############################################################################

alarms = [
        {'id': 1, 'hour': 6, 'minute': 30, 'missionType' : '랜덤'},
        {'id': 2, 'hour': 16, 'minute': 38, 'missionType' : '사진 매칭'}
        ]
nextId = 3

### fuctions (flask) ##################################################################

# hour select options -> 알람 설정할때 뜨는 '시간' 옵션들(1시부터 24시)
def hour_select_options(selected=None):
    
    value_ = ''
    for i in range(1, 25):
        if i == selected:
            value_ = value_+f'<option value="{i:0>2}" selected> {i:0>2} </option>'
        else:
            value_ = value_+f'<option value="{i:0>2}"> {i:0>2} </option>'

    return f'''
        <select name="hour">
            {value_}
        </select>
    '''

# minute select options -> 알람설정할 때 뜨는 '분' 옵션들(00분부터 59분)
def minute_select_options(selected=None):
    
    value_ = ''
    for i in range(00, 60):
        if i == selected:
            value_ = value_+f'<option value="{i:0>2}" selected> {i:0>2} </option>'
        else:
            value_ = value_+f'<option value="{i:0>2}"> {i:0>2} </option>'

    return( f'''
        <select name="minute">
            {value_}
        </select>
    ''')

# 미션 고르는 함수
def misson_select_options(selected=None):

    value_ = ''
    for i in range(1,5):
        if i == selected:
            value_ = value_+f'<option value="{missionType(i)}"selected>{missionType(i)}</option>'
        else:
            value_ = value_+f'<option value="{missionType(i)}">{missionType(i)}</option>'

    return(f'''
        <select name="mission">
            {value_}
        </select>
    ''')

# 미션 숫자 (1,2,3,4)를 문자로 바꾸는 함수
def missionType(typeNum):
    if typeNum == 1:
        return '랜덤'
    elif typeNum == 2:
        return '사진 매칭'
    elif typeNum == 3:
        return '반응속도테스트'
    elif typeNum == 4:
        return '연산'

# missionType 함수의 reverse
def r_missionType(mission):
    if mission == '랜덤':
        return 1
    elif mission == '사진 매칭':
        return 2
    elif mission == '반응속도테스트':
        return 3
    elif mission == '연산':
        return 4




# 템플릿 함수
# template -> 알람 목록
# text -> 본문
def template(content, text, isFuction, id=None):
    update_delete = ''

    if isFuction == 1:
        update_delete =f'''
            <li><a href = /create/>create</a></li>
        '''
    elif isFuction == 2:
        update_delete =f'''
            <li><a href = /create/>create</a></li>
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete" style="background-color:blue; border:none; color:white;"></form></li>
        '''
    return f'''
    <!doctype html>
    <html>
        <head>
            <style>
                #title {{
                    text-decoration: none;
                    color: black;
                }}
                ul li a {{
                    border-style: solid;
                    background-color: blue;
                    text-decoration: none;
                    color: white;
                    margin: 5px;
                    weight: 50px;
                    display: inline-block;
                }}
                ul{{
                    list-style-type: none;  
                }}
            </style>
        <head>
        <body>
            <a href="/" id="title"><strong style="font-size:50px;">일어나야만 하는<br>      이</strong>기혁<strong style="font-size:50px;">유</strong>금진</a>
            <ol>
                {content}
            </ol>
            {text}
            <ul>
                
                {update_delete}
            </ul>
        </body>
    </html>
    '''

def getContents():
    content = ''
    for alarm in alarms:
        content = content+f'''
            <li>
                <a href="/alarm/{(alarm["id"])}/">
                    설정 시간 - {(alarm["hour"]):0>2} : {alarm["minute"]:0>2} - 미션 : {alarm["missionType"]}
                </a>
            </li>
        '''
    return(content)

### routing ###############################################################################################

@app.route('/') # 메인 페이지
def index():
    return template(getContents(),'',1)

@app.route('/alarm/<int:id>/') # 설정된 알람 페이지
def checkalarm(id):
    text = ''
    for alarm in alarms:
        if alarm["id"] == id:
            text = f'{(alarm["hour"])}시 {(alarm["minute"]):0>2}분에 울리는 알람입니다.'
            break

    return template(getContents(), text,2, int(id))
    

@app.route('/create/', methods=['GET', 'POST']) # 알람 생성 페이지
def create():
    global nextId
    if request.method == 'GET':
        text = f'''
            <form action="/create/"method="POST">
                <h2>시간설정</h2>
                {hour_select_options()}시 {minute_select_options()}분
                <h2>미션설정</h2>
                {misson_select_options()}
                <h3>미션 설명</h3>
                <ol>
                    <li><strong>사진 매칭</strong> : OLED에 출력된 단어에 알맞는 사진을 카메라로 인식시킵니다.</li>    
                    <li><strong>반응 속도 테스트</strong> : 불이 들어오면 제한 시간보다 빠르게 버튼을 누릅니다.</li>
                    <li><strong>연산</strong> : 간단한 연산문제를 풉니다.</li>
                </ol>
                <input type="submit" value="저장" style="background-color:blue; border:none; color:white;">
            </form>
        '''
        return template('', text,0)
    elif request.method == 'POST':
        hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        mission = request.form['mission']
        newAlarm =  {'id': nextId, 'hour': hour, 'minute': minute, 'missionType' : mission}
        alarms.append(newAlarm)
        print(alarms)
        return f'''
            <p>{hour}시 {minute}분에 울리는 알람을 저장하였습니다</p>
            <br>
            <a href="/">홈으로 돌아가기</a>
        '''
@app.route('/update/<int:id>/',methods=['GET','POST']) # 알람 업데이트 페이지
def update(id):
    if request.method == 'GET':
        hour = 0
        minute = 0
        mission = ''
        for alarm in alarms:
            if int(id) == alarm['id']:
                hour = alarm['hour']
                minute = alarm['minute']
                mission = r_missionType(alarm['missionType'])

        text = f'''
            <form action="/update/{id}/"method="POST">
                <h2>시간설정</h2>
                {hour_select_options(hour)}시 {minute_select_options(minute)}분
                <h2>미션설정</h2>
                {misson_select_options(mission)}
                <h3>미션 설명</h3>
                <ol>
                    <li><strong>사진 매칭</strong> : OLED에 출력된 단어에 알맞는 사진을 카메라로 인식시킵니다.</li>    
                    <li><strong>반응 속도 테스트</strong> : 불이 들어오면 제한 시간보다 빠르게 버튼을 누릅니다.</li>
                    <li><strong>연산</strong> : 간단한 연산문제를 풉니다.</li>
                </ol>
                <input type="submit" value="저장" style="background-color:blue; border:none; color:white;">
            </form>
        '''
        return template('', text,0)
    elif request.method == 'POST':
        beforeHour = 0
        beforeMinute = 0
        for alarm in alarms:
            if id == alarm['id']:
                beforeHour = alarm['hour']
                beforeMinute = alarm['minute']

        hour = int(request.form['hour'])
        minute = int(request.form['minute'])
        mission = request.form['mission']
        for alarm in alarms:
            if id == alarm['id']:
                alarm['hour'] = hour
                alarm['minute'] = minute
                alarm['missionType'] = mission
                break

        return f'''
            <p>{beforeHour}시 {beforeMinute}분에 울리는 알람을 {hour}시 {minute}분에 울리는 알람으로 수정 완료 하였습니다</p>
            <p>현재 미션 : {mission}</p>
            <br>
            <a href="/">홈으로 돌아가기</a>
        '''

@app.route('/delete/<int:id>/', methods=['POST']) # 알람 삭제
def delete(id):
    for alarm in alarms:
        if id == alarm['id']:
            alarms.remove(alarm)
            break

    return redirect('/')

### functions (Alarm) #######################################################################################

def ringring_alarm(mission_type): # 알람 울리고 미션을 실행하는 함수
    print('제니 : 컴백이 아냐, 떠난 적 없으니까~') #디버깅용 프린트

    #부저 작동 시작
    cry_forever = Process(target=buz.ringAlarm, args= ()) # 알람 울리는 프로세스
    cry_forever.start()

    #미션 실행
    if mission_type== "랜덤":
        #1~3 랜덤 정수를 받아 숫자에 따라 실행하는 미션이 달라진다.
        a = random.randint(1,3)
        if a == 1:  # 1이면 카드 감지 미션
            card_mission.start()
            cry_forever.kill()
        elif a == 2:
            reaction_mission.start()
            cry_forever.kill()
        elif a == 3:
            calcul_mission.start()
            cry_forever.kill()
    
    elif mission_type == "사진 매칭":
        card_mission.start()
        cry_forever.kill()
        
    elif mission_type == "반응속도테스트":
        reaction_mission.start()
        cry_forever.kill()
        
    elif mission_type == "연산":
        calcul_mission.start()
        cry_forever.kill()
        
    now_sec = time.strftime('%S', time.localtime(time.time()))
    time.sleep(60 - int(now_sec)) # 60 - int(now_sec) 만큼 쉬기

def time_checker(): # 시간을 재고 지금 시간과 맞는지 확인해주는 함수

    #무한으로 즐겨요~ 
    while True:
        #현제 시간 체크하기
        now_time = time.strftime('%H시 %M분', time.localtime(time.time()))
        time.sleep(3)

        for alarm in alarms:
            #만약 저장된 알람시각과 현제 시간이 같을 경우 알람을 울리게 한다.
            if f'{alarm["hour"]}시 {alarm["minute"]}분' == now_time:
                ringring_alarm(alarm["missionType"])

                #시계가 정확한지 확인
                print(now_time)
                print(f'{alarm["hour"]}시 {alarm["minute"]}분')
            else:
                pass

### code #################################################################################################

alarm_timing = Thread(target= time_checker, args= ()) # 시간 재는 스레드

if __name__ == '__main__':
    alarm_timing.start() 
    app.run(host='0.0.0.0', threaded= True)
    