import asyncio
import cv2
import websockets
import numpy as np
from argparse import ArgumentParser as argparse

async def server(websocket, path):
    cap = cv2.VideoCapture(0)  # Open video file or capture device. (0) -> webcam

    while True:
        ret, frame = cap.read()  # Read frame
        ret, jpeg = cv2.imencode('.jpg', frame)  # Encode image as JPEG
        data = jpeg.tobytes()  # Convert image to bytes
        await websocket.send(data)  # Send image data over WebSocket

if __name__ == '__main__':
    parser = argparse()
    parser.add_argument('-p', '--port', default='8765', help='Port for broadcasting')
    args = parser.parse_args()

    start_server = websockets.serve(server, 'localhost', args.port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
