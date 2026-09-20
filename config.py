import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key-change-in-production')
    _db_url = os.getenv('DATABASE_URL')
    if _db_url:
        if _db_url.startswith('postgres://'):
            _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
    else:
        if os.getenv('VERCEL') or os.getenv('AWS_LAMBDA_FUNCTION_NAME'):
            _db_url = 'sqlite:////tmp/task_manager.db'
        else:
            _db_url = f"sqlite:///{os.path.join(BASE_DIR, 'task_manager.db')}"


    SQLALCHEMY_DATABASE_URI = _db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False