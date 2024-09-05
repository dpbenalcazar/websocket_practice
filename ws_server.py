import cv2
import torch
import asyncio
import numpy as np
from facenet_pytorch import MTCNN
from PIL import Image, ImageDraw, ImageFont
from websockets.asyncio.server import serve
from argparse import ArgumentParser as argparse

# Constants
cam_mesage = {
    'far': 'Acerquese a la cámara por favor',
    'ok': 'Tomando Foto',
    'close': 'Alejese de la cámara porfavor'
}
msg_xy = {
    'far': (80, 0),
    'ok': (240, 0),
    'close': (100, 0)
}
color = {
    'far': (255, 0, 0),
    'ok': (0, 255, 0),
    'close': (255, 0, 0)
}
font = ImageFont.truetype("arial.ttf", 32)

# Detect if GPU is avalable
#device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')

# Create MTCNN object
mtcnn = MTCNN(keep_all=True, device=device)
print('Running MTCNN on device: {}'.format(device))

async def facial_server(websocket):
    cnt = 0
    face = None

    # Main loop
    while True:
        # Receive frame
        data = await websocket.recv()  # Receive image data
        arr = np.frombuffer(data, np.uint8)  # Convert data to numpy array
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # Decode numpy array into OpenCV frame
            
        try:
            # Convert to pillow image
            frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Find face
            boxes, _ = mtcnn.detect(frame_pil)
            box = boxes[0]

            # Compute box height
            dy = box[3] - box[1]

            # Chose distance range
            if dy < 200: # too far
                dist = 'far'
                cnt = 0
            elif dy >= 200 and dy <270: # perfect distance
                dist = 'ok'
                face = frame_pil.crop(box)
                cnt += 1
            else: # too close
                dist = 'close'
                cnt = 0
            
            # Draw face and info
            draw = ImageDraw.Draw(frame_pil)
            draw.rectangle(box.tolist(), outline=color[dist], width=6)
            draw.text(msg_xy[dist],cam_mesage[dist],color[dist], font=font)

            # Convert back to opencv
            frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_BGR2RGB)
        
        except:
            cnt = 0

        # Send processed frame
        ret, jpeg = cv2.imencode('.jpg', frame)  # Encode image as JPEG
        data = jpeg.tobytes()  # Convert image to bytes
        await websocket.send(data)  # Send image data over WebSocket

        # Check if user quit
        mesage = await websocket.recv()
        if mesage == 'quit':
            print('User quit, no image obtained')
            break

        # Exit on good distance
        if cnt>=10: 
            print('Face image obtained')
            await websocket.send('face obtained')
            break

        # Send continue message
        await websocket.send('continue')

    if face:
        # Send extracted face
        face = cv2.cvtColor(np.array(face), cv2.COLOR_BGR2RGB)
        ret, jpeg = cv2.imencode('.jpg', face)  # Encode image as JPEG
        data = jpeg.tobytes()  # Convert image to bytes
        await websocket.send(data)  # Send image data over WebSocket

    print('Transaction completed')

async def main(port):
    async with serve(facial_server, "0.0.0.0", port):
        await asyncio.get_running_loop().create_future()  # run forever

if __name__ == '__main__':
    parser = argparse()
    parser.add_argument('-p', '--port', default=8765, type=int, help='Port for broadcasting')
    args = parser.parse_args()

    asyncio.run(main(args.port))
