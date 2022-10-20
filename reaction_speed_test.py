# 이 소스 복사해서 나중에 붙여넣을예정
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time
import random

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

GPIO.setwarnings(False)

pwm = GPIO.PWM(piezzo_buzzer, 1)

limit_time = random.randrange(1, 4)

# Raspberry Pi pin configuration:
RST = 24

#디스플레이 세팅
#128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)

# Initialize library.
disp.begin()
width = disp.width
height = disp.height

#Clear display.
disp.clear()
disp.display()

top = 10

def disp_title():
    global width, height, disp, top

    #화면 크기만큼의 빈껍데기 이미지 생성
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    #폰트설정(폰트디자인, 사이즈)
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)

    #이미지 위에 텍스트 출력('This is reaction speed test')
    draw.text((10, top), 'This is', font=font, fill=255)            
    draw.text((10, top+10), 'reaction speed', font=font, fill=255)
    draw.text((10, top+20), 'test!!', font=font, fill=255)

    #이미지를 OLED로 출력
    disp.image(image)
    disp.display()

#동치
def display_times(left_time):
    global width, height, disp, limit_time, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
    draw.text((10, top), 'limit time: {0}'.format(limit_time), font=font, fill=255)
    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
    draw.text((30, top + 20), 'start in', font=font, fill=255)
    draw.text((30, top + 30), '{0} second'.format(left_time), font=font, fill=255)

    disp.image(image)
    disp.display()

# 동치
def disp_mission_start():
    global width, height, disp, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
    draw.text((10, top), 'Mission', font=font, fill=255)
    draw.text((30, top + 20), 'Start', font=font, fill=255)

    disp.image(image)
    disp.display()

#미션 제한시간을 유저에게 알려줌 and 5초 카운트 이후 미션 시작
def wait_mission_and_start():
    for i in range(5, 0, -1):
        display_times(i)
        time.sleep(1)

#미션 실행 함수
def do_mission_untill_clear():
    #전역변수 명시
    global limit_time, button_blue, button_red, button_yellow

    #범위 내 랜덤한 시간동안 대기 이후 led on
    wait_time = random.randrange(1, 6)
    time.sleep(wait_time)

    GPIO.output(led, GPIO.HIGH)

    val_R = GPIO.input(button_red)
    val_Y = GPIO.input(button_yellow)
    val_B = GPIO.input(button_blue)

    #제한 시간 세기 - 미션 시작한 시간 기록
    start_time = time.time()

    #미션을 성공, 실패했는지 확인하는 변수
    is_not_complete = True

    while True:
        #현재 시간 기록
        ing_time = time.time()
        #만약 제한시간이 지나면 무한반복문 빠져나오기
        if ing_time - start_time == limit_time: 
            break
        
        #만약 제한시간 내에 버튼을 눌러 미션을 성공하면 미션 성공으로 변수값 바꿔주고 break
        elif val_R == 1 or val_B == 1 or val_Y == 1:
            is_not_complete == False
            break
    
    #미션 성공, 실패 여부 리턴
    return is_not_complete

disp_title()
time.sleep(3) # 3초만 쉬었다 갑시다~

#미션 제한시간을 유저에게 알려줌 and 5초 카운트 이후 미션 시작
wait_mission_and_start()

disp_mission_start()

#미션을 실패할때까지 미션 실행 함수를 돌린다. 성공, 실패 여부를 함수에서 리턴받음
while True:
    #Flase 리턴받음 == 미션 성공
    if do_mission_untill_clear() == False:
        break
    else:
        #True 리턴받음 == 미션 실패
        disp_mission_failed()
        time.sleep(2)
        limit_time = random.randrange(1, 4)
        wait_mission_and_start()
        
#미션 클리어를 유저에게 보여주는 함수
disp_mission_clear()






