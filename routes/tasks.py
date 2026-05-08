from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db, socketio
from models.task import Task
from analytics.stats import get_analytics

tasks = Blueprint('tasks', __name__)

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
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
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
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    db.session.commit()
    socketio.emit('task_update', {'action': 'updated', 'task': task.to_dict()})
    return jsonify(task.to_dict())

@tasks.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_update', {'action': 'deleted', 'task_id': task_id})
    return jsonify({'message': 'Task deleted'})