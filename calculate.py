from dis import dis
import random
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont


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

def disp_Q(cal_num1, cal_symbol, cal_num2, ans1, ans2, ans3):
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

def disp_res(result):
    global width, height, disp, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
    
    draw.text((10, top), 'Answer', font=font, fill=255)
    draw.text((30, top + 20), '{0}'.format(result), font=font, fill=255)

    disp.image(image)
    disp.display()

def random_exclude(range_start, range_end, excludes):
    r = random.randint(range_start, range_end)
    if r in excludes:
        return random_exclude(range_start, range_end, excludes)
    return r

def operator(number):
    if number == 1:
        return('+')
    elif number == 2:
        return('*')
    elif number == 3:
        return('-')
while True:

    num1 = random.randint(1, 20) # 정수 하나 랜덤
    num2 = random.randint(1, 20) # 정수 하나 랜덤
    c = random.randint(1, 3) # 연산자 랜덤2
    
    if c == 1:
        cal = num1 + num2 # cal -> 계산결과
    elif c == 2: 
        cal = num1 * num2
    elif c == 3:
        cal = num1 - num2

    answer1 = random_exclude(cal-30, cal+30, [cal])
    answer2 = random_exclude(cal-30, cal+30, [cal, answer1])
    answerlist = [answer1, answer2, cal]
    random.shuffle(answerlist)

    disp_Q(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2])

    answer = input('''{0} {1} {2} = ?
        (1:red){3} (2:yellow){4} (3:blue){5}
        >>> '''.format(num1, operator(c), num2, answerlist[0], answerlist[1], answerlist[2]))

    if answerlist[int(answer)-1] == cal:
        print('정답')
        disp_res('Correct')
        break
    else:
        print('오답')
        disp_res('wrong')
            
