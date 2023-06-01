from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread

global capture, switch, out 
capture=1
switch=1

try:
    os.mkdir('./shots')
except OSError as error:
    pass


app = Flask(__name__, template_folder='./templates')


camera = cv2.VideoCapture(0)

def gen_frames():  # generate frame by frame from camera
    
    global out, capture,rec_frame
    while True:
        success, frame = camera.read() 
        if success:
            if(capture):
                capture=0
                now = datetime.datetime.now()
                p = os.path.sep.join(['shots', "plant.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/dar')
def dar():
    return render_template('dar.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
 
        elif  request.form.get('stop') == 'Stop/Start':
            
            if(switch==1):
                switch=0
                camera = cv2.VideoCapture(0)   
            else:
                switch=1
                camera.release()
                cv2.destroyAllWindows()


                 
    elif request.method=='GET':
        return render_template('dar.html')
    return render_template('dar.html')


if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()     