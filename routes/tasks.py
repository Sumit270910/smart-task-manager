from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db, socketio
from models.task import Task
from analytics.stats import get_analytics

tasks = Blueprint('tasks', __name__)

VALID_PRIORITIES = ['low', 'medium', 'high']
VALID_STATUSES = ['pending', 'in_progress', 'completed']

def validate_task(data):
    if not data.get('title') or len(data['title'].strip()) == 0:
        return 'Task title is required!'
    if len(data['title']) > 200:
        return 'Title must be under 200 characters!'
    if data.get('priority') and data['priority'] not in VALID_PRIORITIES:
        return 'Invalid priority value!'
    if data.get('status') and data['status'] not in VALID_STATUSES:
        return 'Invalid status value!'
    return None

@tasks.route('/')
@login_required
def get_tasks_page():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    analytics = get_analytics(current_user.id)
    return render_template('index.html', tasks=all_tasks, analytics=analytics)

@tasks.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([t.to_dict() for t in all_tasks])

@tasks.route('/api/tasks', methods=['POST'])
@login_required
def add_task():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided!'}), 400
    error = validate_task(data)
    if error:
        return jsonify({'error': error}), 400
    task = Task(
        title=data['title'].strip(),
        description=data.get('description', '').strip(),
        priority=data.get('priority', 'medium'),
        status=data.get('status', 'pending'),
        user_id=current_user.id
    )
    db.session.add(task)
    db.session.commit()
    socketio.emit('task_update', {'action': 'added', 'task': task.to_dict()})
    return jsonify(task.to_dict()), 201

@tasks.route('/api/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found!'}), 404
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided!'}), 400
    error = validate_task({**task.to_dict(), **data})
    if error:
        return jsonify({'error': error}), 400
    task.title = data.get('title', task.title).strip()
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    db.session.commit()
    socketio.emit('task_update', {'action': 'updated', 'task': task.to_dict()})
    return jsonify(task.to_dict())

@tasks.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found!'}), 404
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_update', {'action': 'deleted', 'task_id': task_id})
    return jsonify({'message': 'Task deleted successfully!'})