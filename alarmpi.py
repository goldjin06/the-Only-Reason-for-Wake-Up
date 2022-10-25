# 이 소스 복사해서 나중에 붙여넣을예정
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

pwm = GPIO.PWM(piezzo_buzzer, 1)



# 여기부터 소스코드 ################################################################

def playAirplane():
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
    

def melody(name, beat):
    pwm.start()
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
    time.sleep(bear * 0.3)
    pwm.stop()


playAirplane()