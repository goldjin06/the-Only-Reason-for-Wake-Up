from flask import Flask, request
# import RPi as GPIO #디버깅 하려고 일단 주석처리
import time

app = Flask(__name__)












#data

#hour select options -> 알람 설정할때 뜨는 '시간' 옵션들(1시부터 24시)
def hour_select_options():
    
    value_ = ''
    for i in range(1, 25):
        value_ = value_+f'<option value="{i:0>2}"></option>'

    return f'''
        <select title="hour">
            {value_}
        </select>
    '''

#minute select options -> 알람설정할 때 뜨는 '분' 옵션들(00분부터 59분)
def minute_select_options():
    
    value_ = ''
    for i in range(00, 60):
        value_ = value_+f'<option value="{i:0>2}"></option>'

    return( f'''
        <select title="minute">
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
        {'id': 1, 'hour': 6, 'minute': 30, 'missionType' : 1},
        {'id': 2, 'hour': 7, 'minute': 00, 'missionType' : 2}
        ]







# 템플릿 함수
# template -> 알람 목록
# text -> 본문
def template(content, text):
    return f'''
    <!doctype html>
    <html>
        <body>
            <strong>일어나야만 하는 이</strong>(기혁)<strong>유</strong>(금진)
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



#!!!여기서 오류나면 dictionary 자료형 살펴보기!!! 오류 안나면 이 주석 지워줘
@app.route('/')
def index():
    content = ''
    for alarm in alarms:
        content = content+f'''
            <li>
                <a href="/alarm/{(alarm["id"])}/">
                    설정 시간 - {(alarm["hour"]):0>2} : {alarm["minute"]:0>2} - 미션 : {missionType(alarm["missionType"])}
                </a>
            </li>
        '''
    text = ''

    return template(content,text)

@app.route('/alarm/<int:id>/')
def checkalarm(id):
    content = ''
    for alarm in alarms:
        content = content+f'''
            <li>
                <a href="/alarm/{(alarm["id"])}/">
                    설정 시간 - {(alarm["hour"]):0>2} : {alarm["minute"]:0>2} - 미션 : {missionType(alarm["missionType"])}
                </a>
            </li>
        '''
    text = ''
    for alarm in alarms:
        if alarm["id"] == id:
            text = f'{(alarm["hour"])}시 {(alarm["minute"]):0>2}분에 울리는 알람입니다.'
            break

    return template(content, text)
    
# 나중에 만들  크리에이트
# @app.route('/create/', methods=['GET', 'POST'])
# def create():
#     if request.method == 'GET':
#         content = '''
#             <form action="/create/" method="POST">
#                 <p><input type="text" name="title" placeholder="title"></p>
#                 <p><textarea name="body" placeholder="body"></textarea></p>
#                 <p><input type="submit" value="create"></p>
#             </form>
#         '''
#         return

app.run(debug=True)
