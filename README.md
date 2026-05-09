# 📋 Smart Task Manager

A Python-based web application built with Flask, PostgreSQL, WebSockets, and Pandas/NumPy.

## 🚀 Features
- User Registration & Login
- Add, Update, Delete Tasks
- Real-time WebSocket notifications
- Analytics with Pandas & NumPy
- Input validation & error handling
- Clean responsive UI

## 🛠️ Technologies Used
- Python & Flask
- PostgreSQL & Flask-SQLAlchemy
- Flask-Login & Flask-Bcrypt
- Flask-SocketIO (WebSockets)
- Pandas & NumPy
- HTML & CSS

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Sumit270910/smart-task-manager.git
cd smart-task-manager
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create PostgreSQL database
```bash
psql -U postgres
CREATE DATABASE task_manager_db;
\q
```

### 5. Configure environment variables
Create a `.env` file:

### 6. Run the application
```bash
python app.py
```

### 7. Open in browser

## 📊 Database Schema
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
```

## 👨‍💻 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Dashboard |
| GET | /api/tasks | Get all tasks |
| POST | /api/tasks | Add new task |
| PUT | /api/tasks/<id> | Update task |
| DELETE | /api/tasks/<id> | Delete task |
| GET | /login | Login page |
| POST | /login | Login user |
| GET | /register | Register page |
| POST | /register | Register user |
| GET | /logout | Logout user |

## 📁 Project Structure
```
smart_task_manager/
├── app.py
├── config.py
├── .env
├── requirements.txt
├── schema.sql
├── models/
│   ├── user.py
│   └── task.py
├── routes/
│   ├── auth.py
│   └── tasks.py
├── analytics/
│   └── stats.py
├── sockets/
│   └── events.py
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
└── static/
    └── style.css
```

 ## DEMO VIDEO LINK
https://github.com/user-attachments/assets/39a38c52-a7f1-483d-a2ff-1a9a33de3e91





