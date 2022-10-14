from flask import Flask, request
# import RPi as GPIO #디버깅 하려고 일단 주석처리
import time

app = Flask(__name__)

#hour select options -> 알람 설정할때 뜨는 '시간' 옵션들(1시부터 24시)
def hour_select_options():
    
    value_ = ''
    for i in range(1, 25):
        value_ = value_+f'<option value="{i}"></option>'

    return f'''
        <select title="hour">
            {value_}
        </select>
    '''

#minute select options -> 알람설정할 때 뜨는 '분' 옵션들(00분부터 59분)
def minute_select_options():
    
    value_ = ''
    for i in range(00, 60):
        value_ = value_+f'<option value="{i}"></option>'

    return f'''
        <select title="minute">
            {value_}
        </select>
    '''
#이거 마저 작석해야되
def missionType(typeNum):
    if typeNum == 1:
        return '랜덤'
    elif typeNum == 2:
        return '사진 매칭'

#설정한 알람들을 모아둔 list, dictionary
#id는 웹페이지 분류를 위해서
#missionType 1 == random
alarms = [
        {'id': 1, 'hour': 6, 'minute': 30, 'missionType' : 1},
        {'id': 2, 'hour': 7, 'minute': 00, 'missionType' : 2}
        ]

#!!!여기서 오류나면 dictionary 자료형 살펴보기!!! 오류 안나면 이 주석 지워줘
@app.route('/')
def index():
    content = ''
    for alarm in alarms:
         content = content+f'''<li>
                    <a href="/alarm/{(alarm["id"])}/">
                         설정 시간 - {(alarm["hour"])} : {alarm["minute"]} - 미션 : {missionType(alarm["missionType"])}
                     </a>
            </li>
         '''

    return f''' <!doctype html>
    <html>
        <body>
            <strong>일어나야만 하는 이</strong>(기혁)<strong>유</strong>(금진)
            <ol>
                {content}
            </ol>
            <ul>
                #알람 추가, 삭제, 수정 기능
                <li><a href = /create/>create</a></li>
                
            </ul>
        </body>
    </html>
    '''

app.run(debug=True)

