from flask import *
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
import base64
import cv2
from PIL import Image
from PIL import ImageTk
import requests
import os
import numpy as np
import webbrowser
import subprocess
import datetime

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(13,GPIO.OUT)



app = Flask(__name__)



@app.route('/')
def main():
    subprocess.call("sh /home/pi/RPi_Cam_Web_Interface/stop.sh", shell=True)
    return render_template('FirstPage.html')

@app.route('/showidentities')
def showidentities():
    path='/var/www/Identities'
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    fo = open("templates/showidentity.html", "w")

    for imagePath in imagePaths:
        fname=os.path.basename(imagePath)
        c=fname.split('.')
        caption=c[0]
        fo.write( 
'''
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Example</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<div class="thumbnail col-xs-4"><img class="" style="width:200px;height:200px" src="http://localhost/Identities/%s" alt='NoImage'/><div class="caption text-center">%s</div></div>
'''
    %(fname,caption))

    fo.close()
    return render_template('showidentity.html')

    

@app.route('/liveview')
def liveview():
    subprocess.call("sh /home/pi/RPi_Cam_Web_Interface/start.sh", shell=True)
    return redirect('http://localhost/html/min.php')
@app.route('/open')
def Open():
    GPIO.output(13,1)
    time.sleep(1)
    GPIO.output(13,0)
    return render_template('FirstPage.html')



@app.route('/openpage')
def OpenPage():
    return render_template('OP.html')

#GPIO.add_event_detect(18, GPIO.FALLING, callback=OpenPage, bouncetime=100)

@app.route('/newuser')
def NewUser():
    subprocess.call("sudo modprobe bcm2835-v4l2", shell=True)
    time.sleep(2)
    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    path = 'dataSet'
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        #Id = int(os.path.split(imagePath)[-1].split(".")[1])
        Id = os.path.basename(imagePath).split('.')[1]
    Id = str(Id+1)
    sampleNum = 0
    while (True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            # incrementing sample number
            sampleNum = sampleNum + 1
            # saving the captured face in the dataset folder
            cv2.imwrite("dataSet/User." + Id + '.' + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])

        # wait for 100 miliseconds
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        # break if the sample number is morethan 20
        elif sampleNum > 50:
            break
    cam.release()
    requests.post('http://thingtalk.ir/update?key=T9266OS74S5P7BNH', data={"field1": Id})
    with open("dataSet/User.%s.2.jpg"%Id, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    requests.post('http://thingtalk.ir/images?key=3Y9CMUK7MS7MTW8B',data={"image": encoded_string})
    return render_template('FirstPage.html')
    
@app.route('/newidentity')
def NewIdentity():
    recognizer = cv2.createLBPHFaceRecognizer()
    detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml");
    path='dataSet'
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)] 
    #create empth face list
    faceSamples=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        #Id=int(os.path.split(imagePath)[-1].split(".")[1])
        Id = int(os.path.basename(imagePath).split('.')[1])
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp, 1.2, 5)
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    faces = faceSamples
    recognizer.train(faces, np.array(Ids))
    recognizer.save('trainner/trainner.yml')
    return render_template('FirstPage.html')

@app.route('/close')
def close():
    subprocess.call("killall chromium-browser", shell=True)

if __name__ == "__main__":
    app.run()
