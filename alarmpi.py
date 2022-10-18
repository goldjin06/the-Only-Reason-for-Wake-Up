# 이 소스 복사해서 나중에 붙여넣을예정
import RPi.GPIO as GPIO

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

# if 어쩌구 저쩌구:





def music_1():
    pwm.start(50)
    pwm.ChangeFrequency(192)
    time.sleep(0.5)

    pwm.ChangeFrequency(329)
    time.sleep(0.5)

    pwm.ChangeFrequency(192)
    time.sleep(0.36)

    pwm.ChangeFrequency(329)
    time.sleep(0.12)

    pwm.ChangeFrequency(293)
    time.sleep(0.5)

    pwm.ChangeFrequency(246)
    time.sleep(0.5)

    pwm.ChangeFrequency(261)
    time.sleep(0.5)

    pwm.ChangeFrequency(293)
    time.sleep(0.5)

    pwm.ChangeFrequency(329)
    time.sleep(0.5)

    pwm.ChangeFrequency(262)
    time.sleep(0.36)

    pwm.ChangeFrequency(391)
    time.sleep(0.12)
    pwm.stop()