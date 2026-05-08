from app import socketio
from flask_socketio import emit

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('connected', {'message': 'WebSocket connected!'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')