from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from config import Config
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
socketio = SocketIO(app)

login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_at': str(self.created_at)
        }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_analytics(user_id):
    user_tasks = Task.query.filter_by(user_id=user_id).all()
    if not user_tasks:
        return {'total': 0, 'completed': 0, 'pending': 0, 'in_progress': 0, 'completion_percentage': 0.0}
    df = pd.DataFrame([t.to_dict() for t in user_tasks])
    total = len(df)
    completed = int(np.sum(df['status'] == 'completed'))
    pending = int(np.sum(df['status'] == 'pending'))
    in_progress = int(np.sum(df['status'] == 'in_progress'))
    completion_pct = round(float(completed / total * 100), 2)
    return {'total': total, 'completed': completed, 'pending': pending, 'in_progress': in_progress, 'completion_percentage': completion_pct}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        hashed_pw = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('get_tasks_page'))
        flash('Invalid email or password!', 'danger')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def get_tasks_page():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    analytics = get_analytics(current_user.id)
    return render_template('index.html', tasks=all_tasks, analytics=analytics)

@app.route('/api/tasks', methods=['GET'])
@login_required
def get_tasks():
    all_tasks = Task.query.filter_by(user_id=current_user.id).all()
    return jsonify([t.to_dict() for t in all_tasks])

@app.route('/api/tasks', methods=['POST'])
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

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
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

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    socketio.emit('task_update', {'action': 'deleted', 'task_id': task_id})
    return jsonify({'message': 'Task deleted'})

@socketio.on('connect')
def handle_connect():
    pass

@socketio.on('disconnect')
def handle_disconnect():
    pass

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    socketio.run(app, debug=True)