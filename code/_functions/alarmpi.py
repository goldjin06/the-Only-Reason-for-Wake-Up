
import RPi.GPIO as GPIO
import time
import random

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



pwm = GPIO.PWM(piezzo_buzzer, 1)




def playAirplane(): # 비행기를 재생하는 함수
    beat = 0.3
    melody('mi', 1.5)
    melody('re', 0.5)
    melody('do', 1)
    melody('re', 1)
    for i in range(3):
        melody('mi', 1)
        time.sleep(0.01)
    time.sleep(beat)
    for i in range(3):
        melody('re', 1)
        time.sleep(0.01)
    time.sleep(beat)
    for i in range(3):
        melody('mi', 1)
        time.sleep(0.01) 
    time.sleep(beat) # 떴다떴다비행기날아라날아라
    melody('mi', 1.5)
    melody('re', 0.5)
    melody('do', 1)
    melody('re', 1)
    for i in range(3):
        melody('mi', 1)
        time.sleep(0.01)
    time.sleep(beat)
    for i in range(2):
        melody('re', 1)
        time.sleep(0.01)
    melody('mi', 1)
    melody('re', 1)
    melody('do', 1)
    time.sleep(beat * 3)
    
def playSchoolring(): # 학교종이 땡땡땡을 재생하는 함수
    beat = 0.3
    melody('sol', 1)
    time.sleep(0.01)
    melody('sol', 1)
    melody('la', 1)
    time.sleep(0.01)
    melody('la', 1)
    melody('sol', 1)
    time.sleep(0.01)
    melody('sol', 1)
    melody('mi', 2)
    melody('sol', 1)
    time.sleep(0.01)
    melody('sol', 1)
    melody('mi', 1)
    time.sleep(0.01)
    melody('mi', 1)
    melody('re', 4) # 학교종이땡땡땡 여기모여라
    melody('sol', 1)
    time.sleep(0.01)
    melody('sol', 1)
    melody('la', 1)
    time.sleep(0.01)
    melody('la', 1)
    melody('sol', 1)
    time.sleep(0.01)
    melody('sol', 1)
    melody('mi', 2)
    melody('sol', 1)
    melody('mi', 1)
    melody('re', 1)
    melody('mi', 1)
    melody('do', 4)

def melody(name, beat): # 계이름과 박자를 입력하면 음을 재생하는 함수
    
    pwm.start(5)
    if name == 'do':
        pwm.ChangeFrequency(262)
    elif name == 're':
        pwm.ChangeFrequency(294)
    elif name == 'mi':
        pwm.ChangeFrequency(330)
    elif name == 'fa':
        pwm.ChangeFrequency(349)
    elif name == 'sol':
        pwm.ChangeFrequency(392)
    elif name == 'la':
        pwm.ChangeFrequency(440)
    elif name == 'si':
        pwm.ChangeFrequency(494)

    time.sleep(beat * 0.3)
    pwm.stop()

def ringAlarm(): # 랜덤값 받아서 랜덤으로 알람 재생하는 함수
    a = random.randint(1, 2)
    print(a)

    if a == 1:
        while True:
            playSchoolring()
            
    else:
        while True:
            playAirplane()