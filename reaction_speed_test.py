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

# Raspberry Pi pin configuration:
RST = 24

#128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
# Initialize library.
disp.begin()
width = disp.width
height = disp.height
# while True:
#Clear display.
disp.clear()
disp.display()

top = 10
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)

#화면 크기만큼의 빈껍데기 이미지 생성
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#이미지 위에 텍스트 출력('This is reaction speed test')
draw.text((10, top), 'This is', font=font, fill=255)
draw.text((10, top+10), 'reaction speed', font=font, fill=255)
draw.text((10, top+20), 'test!!', font=font, fill=255)

#이미지를 OLED로 출력
disp.image(image)
disp.display()

#5초만 쉬었다 갑시다~
time.sleep(3)

#1에서 4까지의 무직위의 정수를 선택해 선택된 시간 이내에 버튼을 눌러야 한다.
limit_time = random.randrange(1, 4) 


#화면 크기만큼의 빈껍데기 이미지 생성
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#이미지 위에 텍스트 출력(limit time) 
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
draw.text((10, top), 'limit time: {0}'.format(limit_time), font=font, fill=255)
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
draw.text((30, top + 20), 'start in', font=font, fill=255)
draw.text((30, top + 30), '5 second', font=font, fill=255)

#이미지를 OLED로 출력
disp.image(image)
disp.display()

time.sleep(1)

#화면 크기만큼의 빈껍데기 이미지 생성
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#이미지 위에 텍스트 출력(limit time) 
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
draw.text((10, top), 'limit time: {0}'.format(limit_time), font=font, fill=255)
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
draw.text((30, top + 20), 'start in', font=font, fill=255)
draw.text((30, top + 30), '4 second', font=font, fill=255)

#이미지를 OLED로 출력
disp.image(image)
disp.display()

time.sleep(1)

#화면 크기만큼의 빈껍데기 이미지 생성
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#이미지 위에 텍스트 출력(limit time) 
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
draw.text((10, top), 'limit time: {0}'.format(limit_time), font=font, fill=255)
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
draw.text((30, top + 20), 'start in', font=font, fill=255)
draw.text((30, top + 30), '3 second', font=font, fill=255)

#이미지를 OLED로 출력
disp.image(image)
disp.display()

time.sleep(1)

#화면 크기만큼의 빈껍데기 이미지 생성
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#이미지 위에 텍스트 출력(limit time) 
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
draw.text((10, top), 'limit time: {0}'.format(limit_time), font=font, fill=255)
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
draw.text((30, top + 20), 'start in', font=font, fill=255)
draw.text((30, top + 30), '2 second', font=font, fill=255)

#이미지를 OLED로 출력
disp.image(image)
disp.display()

time.sleep(1)

#화면 크기만큼의 빈껍데기 이미지 생성
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

#이미지 위에 텍스트 출력(limit time) 
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 15)
draw.text((10, top), 'limit time: {0}'.format(limit_time), font=font, fill=255)
font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 13)
draw.text((30, top + 20), 'start in', font=font, fill=255)
draw.text((30, top + 30), '1 second', font=font, fill=255)

time.sleep(1)
#미션 시작!

#이미지를 OLED로 출력
disp.image(image)
disp.display()


image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
draw.text((10, top), 'Mission', font=font, fill=255)
draw.text((30, top + 20), 'Start', font=font, fill=255)

disp.image(image)
disp.display()


