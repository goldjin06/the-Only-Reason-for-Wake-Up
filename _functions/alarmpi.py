

# 여기부터 소스코드 ################################################################

def playAirplane():
    print("111")
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
    
def playSchoolring():
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

def melody(name, beat):
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

def ringAlarm():
    a = random.randint(1, 2)
    print(a)

    if a == 1:
        while True:
            playSchoolring()
    else:
        while True:
            playAirplane()

