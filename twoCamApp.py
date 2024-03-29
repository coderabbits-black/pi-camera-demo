# Web streaming example
# Source code from the official PiCamera package
# http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

import cv2
from PIL import Image
from io import BytesIO
from flask import Flask, Response
from CameraService import CameraService

app = Flask(__name__)
cap = CameraService(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.start()

cap1 = CameraService(1)
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap1.start()

PAGE = """\
<html>
<head>
<title>Raspberry Pi - Surveillance Camera</title>
</head>
<body>
<center><h1>Raspberry Pi - Surveillance Camera</h1></center>
<center><img src="stream.mjpg" width="640" height="480"></center>
<center><img src="stream1.mjpg" width="640" height="480"></center>
</body>
</html>
"""


@app.route("/")
def hello_world():
    return PAGE


def cameraRead(camera):
    while True:
        frame = camera.read()
        if frame is not None:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            jpg = Image.fromarray(imgRGB)
            content = BytesIO()
            jpg.save(content, 'JPEG')
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + content.getvalue() + b'\r\n')


@app.route('/stream.mjpg')
def stream():
    response = Response(cameraRead(cap),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return response


@app.route('/stream1.mjpg')
def stream1():
    response = Response(cameraRead(cap1),
                        mimetype='multipart/x-mixed-replace; boundary=frame')
    return response


if __name__ == '__main__':
    app.run(threaded=True)
