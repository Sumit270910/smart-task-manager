try:
    import pandas as pd
    import numpy as np
except ImportError:
    pd = None
    np = None

def get_analytics(user_id):
    from models.task import Task
    user_tasks = Task.query.filter_by(user_id=user_id).all()
    if not user_tasks:
        return {
            'total': 0,
            'completed': 0,
            'pending': 0,
            'in_progress': 0,
            'completion_percentage': 0.0
        }
    total = len(user_tasks)
    completed = sum(1 for t in user_tasks if t.status == 'completed')
    pending = sum(1 for t in user_tasks if t.status == 'pending')
    in_progress = sum(1 for t in user_tasks if t.status == 'in_progress')
    completion_pct = round(float(completed / total * 100), 2) if total > 0 else 0.0
    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
        'completion_percentage': completion_pct
    }