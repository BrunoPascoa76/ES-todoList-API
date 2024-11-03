from data.task import Task
from data import Session,engine

def get_tasks_by_user_id(user_id):
    with Session(engine) as session:
        return session.query(Task).filter(Task.user_id==user_id).all()

def get_task_by_id(id,user_id):
    pass

def add_task(user_id,title,description=None,deadline=None,category="default",priority=0):
    pass

def mark_as_completed(user_id,task_id):
    pass

def update_task(user_id,task_id,title=None,description=None,deadline=None,category=None,is_completed=None):
    pass

def delete_task(user_id,task_id):
    pass