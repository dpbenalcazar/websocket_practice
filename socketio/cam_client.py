import cv2
import socketio
import base64
import numpy as np

# Initialize SocketIO client
sio = socketio.Client()

# Function to encode image to base64
def encode_image(img):
    _, buffer = cv2.imencode('.jpg', img)
    img_data = base64.b64encode(buffer).decode('utf-8')
    return img_data

# Function to decode base64 image
def decode_image(img_data):
    img_data = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
    return img

# Handle connection event
@sio.event
def connect():
    print('Connected to server')

# Handle disconnection event
@sio.event
def disconnect():
    print('Disconnected from server')

# Handle processed frame event
@sio.event
def processed_frame(data):
    # Decode the received frame
    frame = decode_image(data)
    
    # Display the processed frame
    cv2.imshow('Processed Frame', frame)
    cv2.waitKey(1)

# Connect to the server
sio.connect('http://localhost:5000')

# Capture webcam frames and send to server
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # Encode the frame and send to server
    encoded_frame = encode_image(frame)
    sio.emit('frame', encoded_frame)
    
    # Display the original frame
    cv2.imshow('Original Frame', frame)
    if cv2.waitKey(1000) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
sio.disconnect()
