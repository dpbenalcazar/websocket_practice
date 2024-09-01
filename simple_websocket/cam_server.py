import asyncio
import cv2
import websockets
import numpy as np
from websockets.asyncio.server import serve
from argparse import ArgumentParser as argparse

async def cam_server(websocket): # ,path
    cap = cv2.VideoCapture(0)  # Open video file or capture device. (0) -> webcam

    while True:
        ret, frame = cap.read()  # Read frame
        ret, jpeg = cv2.imencode('.jpg', frame)  # Encode image as JPEG
        data = jpeg.tobytes()  # Convert image to bytes
        await websocket.send(data)  # Send image data over WebSocket
        loop_manage = await websocket.recv()
        if loop_manage == 'stop':
            break

async def main(port):
    async with serve(cam_server, "0.0.0.0", port):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == '__main__':
    parser = argparse()
    parser.add_argument('-p', '--port', default=8765, type=int, help='Port for broadcasting')
    args = parser.parse_args()

    #start_server = websockets.serve(cam_server, '0.0.0.0', args.port)

    #asyncio.get_event_loop().run_until_complete(start_server)
    #asyncio.get_event_loop().run_forever()

    asyncio.run(main(args.port))
