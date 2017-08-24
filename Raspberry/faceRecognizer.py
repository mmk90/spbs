import cv2
import numpy as np
from picamera import PiCamera

recognizer = cv2.createLBPHFaceRecognizer()
recognizer.load('trainner/trainner.yml')
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);



font = cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1)
camera=PiCamera()
camera.resolution=(500,500)
camera.capture('MyImage.jpg')
im=cv2.imread('MyImage.jpg')
gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
faces=faceCascade.detectMultiScale(gray, 1.2,5)
for(x,y,w,h) in faces:
    cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
    Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
    if(conf<50):
        if(Id==1):
            Id="Anirban"
        elif(Id==2):
            Id="Mahdi"
        print('Door is open')
    else:
        Id="Unknown"
        print('Door is close')
    cv2.cv.PutText(cv2.cv.fromarray(im),str(Id), (x,y+h),font, 255)
cv2.imshow('im',im)
cv2.waitKey(0)
cv2.destroyAllWindows()

