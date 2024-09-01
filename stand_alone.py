import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

from facenet_pytorch import MTCNN

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
cnt = 0
face = None
font = ImageFont.truetype("arial.ttf", 32)

# Detect if GPU is avalable
#device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
print('Running MTCNN on device: {}'.format(device))

# Create MTCNN object
mtcnn = MTCNN(keep_all=True, device=device)

# Create window
cv2.namedWindow("face-recognition")
vc = cv2.VideoCapture(0)

# try to get the first frame
if vc.isOpened(): 
    rval, frame = vc.read()
else:
    rval = False
print('Camera online')

# Main loop
while rval:
    # Read frame
    rval, frame = vc.read()

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

    # Display frame
    cv2.imshow("face-recognition", frame)

    if cnt>=10: # exit on good distance
        print('Face image obtained')
        break

    key = cv2.waitKey(20)
    if key in [27, 81, 113]: # exit on ESC or Q
        print('User quit, no image obtained')
        break


vc.release()
cv2.destroyWindow("face-recognition")

if face:
    plt.imshow(face)
    plt.title('Rostro Capturado')
    plt.show()

print('Done!')