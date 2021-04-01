import cv2
import numpy
import time
from gpiozero import LED

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)
kit.servo[1].angle = 0

# def detectCascade(frame):
#     imageCopy = frame
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     cascade =cv2.CascadeClassifier( "cat.xml")
#     detectedCat = cascade.detectMultiScale(gray,1.2,9)
#     for bbox in detectedCat:
#         x,y,w,h =bbox
#         cv2.rectangle(frame, (x,y),(x+w, y+h),(0,0,255),3)

cap = cv2.VideoCapture(0)
cap.set(3, 480)
cap.set(4, 320)

ret, frame = cap.read()
frame = cv2.resize(frame,None, fx =.5, fy =.5, interpolation = cv2.INTER_AREA)
rows, cols, _ = frame.shape
sprayer = LED(21)
counter = 0
box_area =0
spray_area = 80000
x_medium = int(cols / 2)
center = int(cols / 2)

y_medium = int(rows/2)
y_center = int(rows/2)
position = 90 # degrees
y_position = 20
i = 0
increasing = True
kit.servo[0].angle = position

while(True):
    ret,frame = cap.read()
    frame = cv2.resize(frame,None, fx =.5, fy =.5, interpolation = cv2.INTER_AREA)
    imageCopy = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cascade =cv2.CascadeClassifier( "cat.xml")
    detectedCat = cascade.detectMultiScale(gray,1.1,2)
    for bbox in detectedCat:
        x,y,w,h =bbox
        cv2.rectangle(frame, (x,y),(x+w, y+h),(0,0,255),3)
        x_medium =int((x + x + w) / 2)
        y_medium = int((y + y + h)/2)
        box_area = (x+w)*(y+h)
        break
    # cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)


    # Move servo motor
    if(box_area > 0):
        if x_medium < center -50:
            position -= 2
        elif x_medium > center + 50:
            position += 2
        if y_medium < y_center -50:
            y_position += 2
        elif y_medium > y_center + 50:
            y_position -= 2
        
        kit.servo[0].angle = position
        kit.servo[1].angle = y_position
   
    if ( box_area > spray_area):
        if(counter >= 30):
            print("sprayer on")
            time.sleep(1)
            print("sprayer off")
        else:
            counter += 10
    else:
        if (counter > 0):
            counter -= 1
    box_area =0

    # cv2.line(frame, (x_medium, 0), (x_medium, 480), (0, 255, 0), 2)
    cv2.imshow('test', frame)
    c = cv2.waitKey(1)
    if(c == 27):
        break

    # kit.servo[0].angle = i
    # if( i == 180):
    #     increasing = False
    # if( i == 0):
    #     increasing = True
    # if(increasing):
    #     i = i+2
    # else:
    #     i = i-2
cap.release()
cv2.destroyAllWindows()


