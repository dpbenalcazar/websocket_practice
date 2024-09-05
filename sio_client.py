import cv2
import asyncio
import socketio
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser as argparse

# Define global variables
global p_frame, face
p_frame = None
face = None

# Create a Socket.IO client
sio = socketio.Client()
    
# Define an event handler for connection
@sio.event
def connect():
    print('Connected to server')

# Define an event handler for disconnection
@sio.event
def disconnect():
    print('Disconnected from server')

# Define an event handler reading webcam
@sio.event
def receive_frame(data):  
    global p_frame, continuar
     # Receive processed frame from server
    arr = np.frombuffer(data, np.uint8)  # Convert data to numpy array
    p_frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Decode numpy array into OpenCV frame
    continuar = True

@sio.event
def receive_face(data):  
    global face
    # Receive processed frame from server
    arr = np.frombuffer(data, np.uint8)  # Convert data to numpy array
    data = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Decode numpy array into OpenCV frame
    face = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
    print('Face Received!')
    print(face.shape)

def client_main():
    global p_frame, face, continuar
    
    # Create window
    cv2.namedWindow("face-recognition")
    vc = cv2.VideoCapture(0)

    # try to get the first frame
    if vc.isOpened(): 
        rval, p_frame = vc.read()
    else:
        rval = False
    print('Camera online')

    while rval:
        # Read frame
        rval, frame = vc.read()
        
        # Send frame to serer
        ret, jpeg = cv2.imencode('.jpg', frame)  # Encode image as JPEG
        data = jpeg.tobytes()  # Convert image to bytes
        sio.emit('process_frame', data)
        continuar = False

        # Display processed frame
        while not continuar:
            pass
        cv2.imshow("face-recognition", p_frame)

        # Check if user wants to quit
        key = cv2.waitKey(10)
        if key in [27, 81, 113]: # exit on ESC or Q
            print('User quit, no image obtained')
            break

        # Check server control mesage
        if face is not None:
            print('Face capture successful')
            break

    vc.release()
    cv2.destroyWindow("face-recognition")


if __name__ == '__main__':
    parser = argparse()
    parser.add_argument('-i', '--ip', default='localhost', help='Camera srver IP address')
    parser.add_argument('-p', '--port', default='8765',    help='Camera srver port')
    args = parser.parse_args()

    url = 'http://{}:{}'.format(args.ip, args.port)

    sio.connect(url)
    client_main()
    while face is None:
        pass
    sio.disconnect()
    # Show face image
    plt.imshow(face)
    plt.title('Rostro Capturado')
    plt.show()
    print('Done!')
    
    