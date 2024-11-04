from data.task import Task
from data import engine
from sqlalchemy.orm import Session,make_transient

def get_tasks_by_user_id(user_id):
    with Session(engine,expire_on_commit=False) as session:
        tasks=session.query(Task).filter(Task.user_id==user_id).all()
        return tasks

def get_task_by_id(id,user_id):
    pass

def add_task(user_id,title,description=None,deadline=None,category="default",priority=0):
    with Session(engine,expire_on_commit=False) as session:
        task=Task(user_id=user_id,title=title,description=description,deadline=deadline,category=category,priority=priority)
        session.add(task)
        session.commit()
        session.refresh(task)
        make_transient(task)
    return task

def mark_as_completed(user_id,task_id):
    pass

def update_task(user_id,task_id,title=None,description=None,deadline=None,category=None,is_completed=None):
    pass

def delete_task(user_id,task_id):
    pass