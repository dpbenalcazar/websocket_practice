import cv2
import torch
import numpy as np
from PIL import Image, ImageDraw
from facenet_pytorch import MTCNN

# Detect if GPU is avalable
#device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')
print('Running MTCNN on device: {}'.format(device))

# Create MTCNN object
mtcnn = MTCNN(keep_all=True, device=device)

# Create window
cv2.namedWindow("webcam mtcnn")
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
        
        # Draw faces
        draw = ImageDraw.Draw(frame_pil)
        for box in boxes:
            draw.rectangle(box.tolist(), outline=(255, 0, 0), width=6)

        # Convert back to opencv
        frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_BGR2RGB)
    except:
        pass

    # Display frame
    cv2.imshow("webcam mtcnn", frame)

    key = cv2.waitKey(20)
    if key in [27, 81, 113]: # exit on ESC or Q
        print('User quit')
        break

cv2.destroyWindow("webcam mtcnn")
vc.release()