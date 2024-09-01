import cv2
import asyncio
import websockets
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser as argparse

async def client(ip='localhost', port='8765'):
    uri = "ws://{}:{}".format(ip, port)
    face = None
    
    # Create window
    cv2.namedWindow("face-recognition")
    vc = cv2.VideoCapture(0)

    # try to get the first frame
    if vc.isOpened(): 
        rval, frame = vc.read()
    else:
        rval = False
    print('Camera online')

    async with websockets.connect(uri) as websocket:
        while rval:
            # Read frame
            rval, frame = vc.read()
            
            # Send frame to serer
            ret, jpeg = cv2.imencode('.jpg', frame)  # Encode image as JPEG
            data = jpeg.tobytes()  # Convert image to bytes
            await websocket.send(data)  # Send image data over WebSocket

            # Receive processed frame from server
            data = await websocket.recv()  # Receive image data
            arr = np.frombuffer(data, np.uint8)  # Convert data to numpy array
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Decode numpy array into OpenCV frame

            # Display frame
            cv2.imshow("face-recognition", frame)

            # Check if user wants to quit
            key = cv2.waitKey(20)
            if key in [27, 81, 113]: # exit on ESC or Q
                await websocket.send('quit')
                print('User quit, no image obtained')
                break
            else:
                await websocket.send('continue')

            # Check server control mesage
            mesage = await websocket.recv()
            if mesage == 'face obtained':
                print('Face capture successful')
                face = True
                break

        vc.release()
        cv2.destroyWindow("face-recognition")

        if face:
            # Receive best face
            data = await websocket.recv()  # Receive image data
            arr = np.frombuffer(data, np.uint8)  # Convert data to numpy array
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Decode numpy array into OpenCV frame
            face = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 

            # Show face image
            plt.imshow(face)
            plt.title('Rostro Capturado')
            plt.show()

        print('Done!')

if __name__ == '__main__':
    parser = argparse()
    parser.add_argument('-i', '--ip', default='localhost', help='Camera srver IP address')
    parser.add_argument('-p', '--port', default='8765',    help='Camera srver port')
    args = parser.parse_args()

    #asyncio.get_event_loop().run_until_complete(client(args.ip, args.port))
    asyncio.run(client(args.ip, args.port))