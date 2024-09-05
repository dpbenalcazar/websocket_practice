import asyncio
import cv2
import numpy as np
import websockets
from argparse import ArgumentParser as argparse

async def client(ip='localhost', port='8765'):
    uri = "ws://{}:{}".format(ip, port)
    async with websockets.connect(uri) as websocket:
        while True:
            data = await websocket.recv()  # Receive image data
            arr = np.frombuffer(data, np.uint8)  # Convert data to numpy array
            frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Decode numpy array into OpenCV frame
            cv2.imshow('Client Camera', frame)  # Display frame
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                await websocket.send('stop')
                break
            else:
                await websocket.send('continue')
        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse()
    parser.add_argument('-i', '--ip', default='localhost', help='Camera srver IP address')
    parser.add_argument('-p', '--port', default='8765',    help='Camera srver port')
    args = parser.parse_args()

    #asyncio.get_event_loop().run_until_complete(client(args.ip, args.port))
    asyncio.run(client(args.ip, args.port))
