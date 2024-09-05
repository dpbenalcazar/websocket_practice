import socketio

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

# Define an event handler for chat messages
@sio.event
def chat_message(data):
    print('Message from', data['user_id'], ':', data['message'])

# Define an event handler for user joined
@sio.event
def user_joined(data):
    print('User joined:', data['user_id'])

# Define an event handler for user left
@sio.event
def user_left(data):
    print('User left:', data['user_id'])

if __name__ == '__main__':
    sio.connect('http://localhost:5000')
    sio.emit('chat_message', 'Hello everyone!')
    #sio.wait()
    sio.sleep(10)
    sio.disconnect()
