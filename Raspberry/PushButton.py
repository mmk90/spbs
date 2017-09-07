from picamera import PiCamera
import RPi.GPIO as GPIO
import webbrowser
import time
import subprocess
import base64
import requests
import os
import numpy as np
import cv2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.OUT)
    
def on_publish(client, userdata, mid):
    print("mid: "+str(mid))

def on_subscribe(client, userdata, mid, granted_qos):
    s = "Subscribed: "+str(mid)+" "+str(granted_qos)
 
def on_message(client, userdata, msg):
        if msg.payload=="open":
            GPIO.output(13,1)
            time.sleep(1)
            GPIO.output(13,0)
            
def MaxRepeat(li):
    st = set(li)
    mx = -1
    for each in st:
        temp = li.count(each)
        if mx < temp:
            mx = temp 
            h = each 
    return h

while True:
    if GPIO.input(18) == False:
        time.sleep(0.2)
        while GPIO.input(18) == False:
            continue
        camera=PiCamera()
        camera.resolution=(400,400)
        camera.capture('/var/www/htmlimg/MyImage.jpg')
        camera.close()
        subprocess.call("chromium-browser http://localhost:5000/openpage --start-fullscreen", shell=True)
        with open("/var/www/htmlimg/MyImage.jpg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        requests.post('http://thingtalk.ir/images?key=GGM5LXID6LQ4WERI',data={"image": encoded_string})

        subprocess.call("sudo modprobe bcm2835-v4l2", shell=True)
        recognizer = cv2.createLBPHFaceRecognizer()
        recognizer.load('trainner/trainner.yml')
        cascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath);
        lst=[0]
        cam = cv2.VideoCapture(0)
        for x in xrange(6):
            ret, im= cam.read()
            gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(gray, 1.2,5)
            for(x,y,w,h) in faces:
                Id, conf = recognizer.predict(gray[y:y+h,x:x+w])
                if(conf<90):
                    lst.append(Id)
        lst.sort()
        PId=MaxRepeat(lst)
        date=datetime.datetime.now().date().strftime("%Y-%m-%d")
        time=datetime.datetime.now().time().strftime("%H:%M:%S")
        if(PId >= 3):
            requests.post('http://thingtalk.ir/update?key=CHO6MJPC463NSX3D', data={"field1": PId, "field2": date, "field3": time })
        else:
            requests.post('http://thingtalk.ir/update?key=CHO6MJPC463NSX3D', data={"field1": 0, "field2": date, "field3": time  })
    
        
        client = paho.Client()
        client.on_publish = on_publish
        client.connect("thingtalk.ir", 1883)
        client.loop_start()
        (rc, mid) = client.publish("openning", str("111"), qos=1)

        client = paho.Client()
        client.on_subscribe = on_subscribe
        client.on_message = on_message
        client.connect("thingtalk.ir", 1883)
        client.subscribe("opendoor", qos=1)
        client.loop_forever()
    
            
