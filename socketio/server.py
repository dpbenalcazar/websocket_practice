import socketio

# Create a Socket.IO server
sio = socketio.Server()

# Create a WSGI app
app = socketio.WSGIApp(sio)

# Define an event handler for connection
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)
    sio.emit('user_joined', {'user_id': sid})

# Define an event handler for disconnection
@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)
    sio.emit('user_left', {'user_id': sid})

# Define an event handler for chat messages
@sio.event
def chat_message(sid, data):
    print('Message from', sid, ':', data)
    sio.emit('chat_message', {'user_id': sid, 'message': data})

if __name__ == '__main__':
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)