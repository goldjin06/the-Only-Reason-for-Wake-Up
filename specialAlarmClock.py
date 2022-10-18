from flask import Flask, request, redirect
from threading import Thread
#import RPi as GPIO #디버깅 하려고 일단 주석처리
import time
import os

app = Flask(__name__)

alarms = [
        {'id': 1, 'hour': 6, 'minute': 30, 'missionType' : '랜덤'},
        {'id': 2, 'hour': 16, 'minute': 38, 'missionType' : '사진 매칭'}
        ]
nextId = 3


#data

#hour select options -> 알람 설정할때 뜨는 '시간' 옵션들(1시부터 24시)
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

#minute select options -> 알람설정할 때 뜨는 '분' 옵션들(00분부터 59분)
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

#미션 숫자 (1,2,3,4)를 문자로 바꾸는 함수
def missionType(typeNum):
    if typeNum == 1:
        return '랜덤'
    elif typeNum == 2:
        return '사진 매칭'
    elif typeNum == 3:
        return '반응속도테스트'
    elif typeNum == 4:
        return '연산'

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
def template(content, text, id=None):
    update_delete = ''
    if id != None:
        update_delete =f'''
            <li><a href="/update/{id}/">update</a></li>
            <li><form action="/delete/{id}/" method="POST"><input type="submit" value="delete"></form></li>
        '''
    return f'''
    <!doctype html>
    <html>
        <body>
            <a href="/"><strong style="font-size:50px;">일어나야만 하는 이</strong>기혁<strong style="font-size:50px;">유</strong>금진</a>
            <ol>
                {content}
            </ol>
            {text}
            <ul>
                <li><a href = /create/>create</a></li>
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

#!!!여기서 오류나면 dictionary 자료형 살펴보기!!! 오류 안나면 이 주석 지워줘
@app.route('/')
def index():
    return template(getContents(),'')

@app.route('/alarm/<int:id>/')
def checkalarm(id):
    text = ''
    for alarm in alarms:
        if alarm["id"] == id:
            text = f'{(alarm["hour"])}시 {(alarm["minute"]):0>2}분에 울리는 알람입니다.'
            break

    return template(getContents(), text, int(id))
    

@app.route('/create/', methods=['GET', 'POST'])
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
                <input type="submit" value="저장">
            </form>
        '''
        return template('', text)
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
@app.route('/update/<int:id>/',methods=['GET','POST'])
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
                <input type="submit" value="저장">
            </form>
        '''
        return template('', text)
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

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for alarm in alarms:
        if id == alarm['id']:
            alarms.remove(alarm)
            break

    return redirect('/')


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', threaded= True)
#     time_checker()
#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

def ringring_alarm():
    print('컴백이 아냐, 떠난 적 없으니까~') #이곳에 gpio 코드 넣기
    now_sec = time.strftime('%S', time.localtime(time.time()))
    time.sleep(60 - int(now_sec))

def time_checker():
    while True:
        now_time = time.strftime('%H시 %M분', time.localtime(time.time()))
        time.sleep(3)
        for alarm in alarms:
            if f'{alarm["hour"]}시 {alarm["minute"]}분' == now_time:
                ringring_alarm()
                print(now_time)
                print(f'{alarm["hour"]}시 {alarm["minute"]}분')
            else:
                pass

alarm_timing = Thread(target= time_checker, args= ())

if __name__ == '__main__':
    alarm_timing.start()
    app.run(host='0.0.0.0', threaded= True)
    


#ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

# def clock():
#     ko_now_time = time.strftime('%H시 %M분', time.localtime(time.time()))
#     time.sleep(1)
#     return ko_now_time

# #알람 울리는 함수
# def ringing_alarm():
#     print(f'띠로리 - {clock()}') #~~임시~~

# #알람 울리는 시간 계산
# #만약 현재 시각과 저장해둔 알람의 시간이 일치할 경우 ringing_alarm 함수를 호출한다 == 알람이 울리게 한다
# def when_toAlarm():
#     for alarm in alarms:
#         if f'{alarm["hour"]}시 {alarm["minute"]}분' == str(clock()):
#             ringing_alarm() 


# ing_clock = Thread(target= clock, args= ())
# timing_alarm_check = Thread(target= when_toAlarm, args= ())
# timing_alarm_check.start()
# ing_clock.start()


