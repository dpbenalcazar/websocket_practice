# websocket_practice
Face detection API with MTCNN y Websockets. 

## Installation

#### 1) Create a pytorch environment
```bash
conda create -n pytorch python=3.11
conda activate pytorch
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

#### 2) Install Facenet
```bash
pip install facenet-pytorch
```

#### 3) Install the rest of the requirements
```bash
pip install -r requirements.txt
```

## Stand Alone Example
The **stand_alone.py** code runs an example of the basic face recognition system without communications.
```bash
conda activate pytorch
python stand_alone.py
```

## Websocket API
To run the app using python websockets. The client sends the frames to the server and plots the processed frames. The server uses MTCNN to find the biggest face in each frame.

To run the server:
```bash
conda activate pytorch
python ws_server.py
```
To run the client:
```bash
conda activate pytorch
python ws_client.py
```

## Socket.IO API
To run the app using python socketio. The client sends the frames to the server and plots the processed frames. The server uses MTCNN to find the biggest face in each frame.

To run the server:
```bash
conda activate pytorch
python sio_server.py
```
To run the client:
```bash
conda activate pytorch
python sio_client.py
```