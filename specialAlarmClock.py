from flask import Flask, request
# import RPi as GPIO #디버깅 하려고 일단 주석처리
import time

app = Flask(__name__)












#data

#hour select options -> 알람 설정할때 뜨는 '시간' 옵션들(1시부터 24시)
def hour_select_options():
    
    value_ = ''
    for i in range(1, 25):
        value_ = value_+f'<option value="{i:0>2}"> {i:0>2} </option>'

    return f'''
        <select name="hour">
            {value_}
        </select>
    '''

#minute select options -> 알람설정할 때 뜨는 '분' 옵션들(00분부터 59분)
def minute_select_options():
    
    value_ = ''
    for i in range(00, 60):
        value_ = value_+f'<option value="{i:0>2}"> {i:0>2} </option>'

    return( f'''
        <select name="minute">
            {value_}
        </select>
    ''')

# 미션 고르는 함수
def misson_select_options():

    value_ = ''
    for i in range(1,5):
        value_ = value_+f'<option value="{missionType(i)}">{missionType(i)}</option>'

    return(f'''
        <select name="mission">
            {value_}
        </select>
    ''')

#이거 마저 작석해야되 -> 작성완료
def missionType(typeNum):
    if typeNum == 1:
        return '랜덤'
    elif typeNum == 2:
        return '사진 매칭'
    elif typeNum == 3:
        return '반응속도테스트'
    elif typeNum == 4:
        return '연산'

#설정한 알람들을 모아둔 list, dictionary
#id는 웹페이지 분류를 위해서
#missionType 1 == random
alarms = [
        {'id': 1, 'hour': 6, 'minute': 30, 'missionType' : '랜덤'},
        {'id': 2, 'hour': 7, 'minute': 00, 'missionType' : '사진 매칭'}
        ]
nextId = 3







# 템플릿 함수
# template -> 알람 목록
# text -> 본문
def template(content, text):
    return f'''
    <!doctype html>
    <html>
        <body>
            <strong style="font-size:50px;">일어나야만 하는 이</strong>기혁<strong style="font-size:50px;">유</strong>금진
            <ol>
                {content}
            </ol>
            {text}
            <ul>
                알람 추가, 삭제, 수정 기능
                <li><a href = /create/>create</a></li>
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

    return template(getContents(), text)
    

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

app.run(host='0.0.0.0',debug=True)
