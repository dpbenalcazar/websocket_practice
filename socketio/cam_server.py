import cv2
import socketio
import base64
import numpy as np
import eventlet
from flask import Flask

# Initialize Flask app and SocketIO server
app = Flask(__name__)
sio = socketio.Server()
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)

# Function to decode base64 image
def decode_image(img_data):
    img_data = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

# Function to encode image to base64
def encode_image(img):
    _, buffer = cv2.imencode('.jpg', img)
    img_data = base64.b64encode(buffer).decode('utf-8')
    return img_data

# Handle connection event
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

# Handle disconnection event
@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

# Handle frame event
@sio.event
def frame(sid, data):
    # Decode the received frame
    frame = decode_image(data)
    
    # Process the frame (convert to grayscale)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Encode the processed frame and send it back to the client
    encoded_frame = encode_image(gray_frame)
    sio.emit('processed_frame', encoded_frame, to=sid)

# Run the Flask app with eventlet
if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
