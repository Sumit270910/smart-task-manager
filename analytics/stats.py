import pandas as pd
import numpy as np
from models.task import Task

def get_analytics(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()
    
    if not tasks:
        return {
            'total': 0,
            'completed': 0,
            'pending': 0,
            'in_progress': 0,
            'completion_percentage': 0.0
        }

    df = pd.DataFrame([t.to_dict() for t in tasks])

    total = len(df)
    completed = int(np.sum(df['status'] == 'completed'))
    pending = int(np.sum(df['status'] == 'pending'))
    in_progress = int(np.sum(df['status'] == 'in_progress'))
    completion_pct = round(float(np.divide(completed, total) * 100), 2)

    return {
        'total': total,
        'completed': completed,
        'pending': pending,
        'in_progress': in_progress,
        'completion_percentage': completion_pct
    }