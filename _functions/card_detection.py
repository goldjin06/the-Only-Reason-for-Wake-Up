import cv2
import numpy as np
import time
import random
from operator import is_not
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import RPi.GPIO as GPIO

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

def disp_mission_start(selected_picture):
    global width, height, disp, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
    draw.text((10, top), 'detect', font=font, fill=255)
    draw.text((30, top + 20), selected_picture, font=font, fill=255)

    disp.image(image)
    disp.display()
    
def mission_complete():
    global width, height, disp, top

    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 25)
    draw.text((10, top), 'MISSION', font=font, fill=255)
    draw.text((30, top + 20), 'COMPLETE', font=font, fill=255)

    disp.image(image)
    disp.display()

def detection(img):
    blob = cv2.dnn.blobFromImage(img, scalefactor=1, size=(224, 224), mean=(104, 117, 123))



# blob 이미지를 네트워크 입력으로 설정
    net.setInput(blob)

    # 네트워크 실행 (순방향)
    detections = net.forward()

    # 가장 높은 값을 가진 클래스 얻기
    out = detections.flatten()
    classId = np.argmax(out)
    confidence = out[classId]

    # 분류 결과 출력

    text = '%s (%4.2f%%)' % (classNames[classId], confidence * 100)
    cv2.putText(img, text, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
    
    return classNames[classId]


# model, config, classFile 설정
model = './dnn/bvlc_googlenet.caffemodel'
config = './dnn/deploy.prototxt'
classFile = './dnn/classification_classes_ILSVRC2012.txt'

classNames = None
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Load a pre-trained neural network
net = cv2.dnn.readNet(model, config)

# 이미지 파일 읽기
cap = cv2.VideoCapture(0)


###### 여기부터 소스코드 #################################################################

picture = ['teddy, teddy bear', 'banana', 'daisy']
random.shuffle(picture)

selected_picture = picture[0]
print("**detect {0}**".format(selected_picture))
disp_mission_start(selected_picture)

while True:
    if not cap.isOpened():
        print('Camera open failed')
        exit()

    ret, frame = cap.read()
    if not ret:
        break

    img = frame
    # img = cv2.imread('bear.jpg')
    a = detection(img)
    print(a)

    if a == selected_picture:
        print('완료')
        break

    time.sleep(1)

# blob 이미지 생성
cap.release()
cv2.destroyAllWindows()