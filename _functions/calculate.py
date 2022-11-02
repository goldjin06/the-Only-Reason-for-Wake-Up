from dis import dis
import random
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO
import time

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

def disp_Q(cal_num1, cal_symbol, cal_num2, ans1, ans2, ans3): # OLED에 문제 출력
    global width, height, disp, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 18)
    draw.text((10, top - 5), '{0} {1} {2} = ?'.format(cal_num1, cal_symbol, cal_num2), font=font, fill=255)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
    draw.text((10, top + 14), '(RED) : {0}'.format(ans1), font=font, fill=255)
    draw.text((10, top + 24), '(YEL) : {0}'.format(ans2), font=font, fill=255)
    draw.text((10, top + 34), '(BLU) : {0}'.format(ans3), font=font, fill=255)

    disp.image(image)
    disp.display()

def disp_res(result): # 결과 출력 (틀렸는지 맞았는지)
    global width, height, disp, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
    
    draw.text((10, top), 'Answer', font=font, fill=255)
    draw.text((30, top + 20), '{0}'.format(result), font=font, fill=255)

    disp.image(image)
    disp.display()

def random_exclude(range_start, range_end, excludes): # excludes를 제외한 range_start부터 range_end 까지의 랜덤숫자
    r = random.randint(range_start, range_end)
    if r in excludes:
        return random_exclude(range_start, range_end, excludes)
    return r

def operator(number): # 랜덤정수를 연산자로 변환
    if number == 1:
        return('+')
    elif number == 2:
        return('*')
    elif number == 3:
        return('-')

def start():
    # Raspberry Pi pin configuration:
    

    
    

    num1 = random.randint(1, 20) # 정수 하나 랜덤
    num2 = random.randint(1, 20) # 정수 하나 랜덤
    c = random.randint(1, 3) # 연산자 랜덤2
    
    if c == 1:
        cal = num1 + num2 # cal -> 계산결과
    elif c == 2: 
        cal = num1 * num2
    elif c == 3:
        cal = num1 - num2

    answer1 = random_exclude(cal-30, cal+30, [cal]) # 답을 제외한 랜덤숫자 (보기1)
    answer2 = random_exclude(cal-30, cal+30, [cal, answer1]) # 답과 보기1을 제외한 랜덤숫자 (보기2)
    answerlist = [answer1, answer2, cal] # 답, 보기1, 보기2를 배열에 담고 셔플
    random.shuffle(answerlist)

    disp_Q(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2]) # 문제출력
    print(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2])
    while True:
        answer = 0
        red = GPIO.input(button_red) # 버튼 입력
        yellow = GPIO.input(button_yellow)
        blue = GPIO.input(button_blue)

        if red and not yellow and not blue:
            answer = 1
        elif not red and yellow and not blue:
            answer = 2
        elif not red and not yellow and blue:
            answer = 3

        if answerlist[int(answer)-1] == cal: # 정답이 맞는지 확인
            print(answer)
            print('정답')
            disp_res('Correct')
            time.sleep(2)
            break
        elif answer != 0:
            print('오답')
            disp_res('wrong')
            time.sleep(2)
            disp_Q(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2])
    
    disp.clear()



        # answer = input('''{0} {1} {2} = ?
        #     (1:red){3} (2:yellow){4} (3:blue){5}
        #     >>> '''.format(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2]))

    
            
