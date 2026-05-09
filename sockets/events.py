from flask_socketio import emit

def register_events(socketio):
    @socketio.on('connect')
    def handle_connect():
        emit('connected', {'message': 'WebSocket connected!'})

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('task_added')
    def handle_task_added(data):
        emit('task_update', {'action': 'added', 'task': data}, broadcast=True)

    @socketio.on('task_updated')
    def handle_task_updated(data):
        emit('task_update', {'action': 'updated', 'task': data}, broadcast=True)

    @socketio.on('task_deleted')
    def handle_task_deleted(data):
        emit('task_update', {'action': 'deleted', 'task_id': data}, broadcast=True)