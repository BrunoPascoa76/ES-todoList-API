from data.task import Task
from data import engine
from sqlalchemy.orm import Session,make_transient

def get_tasks_by_user_id(user_id):
    with Session(engine,expire_on_commit=False) as session:
        tasks=session.query(Task).filter(Task.user_id==user_id).all()
        return tasks

def get_task_by_id(id,user_id):
    with Session(engine,expire_on_commit=False) as session:
        task=session.query(Task).filter(Task.id==id).first()
        if task is None:
            return None,404
        elif task.user_id!=user_id:
            return None,401
        else:
            return task,200
        
def toggle_completed(task_id,user_id):
    with Session(engine,expire_on_commit=False) as session:
        task=session.query(Task).filter(Task.id==task_id).first()
        if task is None:
            return 404
        elif task.user_id!=user_id:
            return 401
        else:
            task.is_completed=not task.is_completed
            session.commit()
            return 200

def add_task(user_id,title,description=None,deadline=None,category="default",priority=0):
    with Session(engine,expire_on_commit=False) as session:
        task=Task(user_id=user_id,title=title,description=description,deadline=deadline,category=category,priority=priority)
        session.add(task)
        session.commit()
        session.refresh(task)
        make_transient(task)
    return task

def update_task(task_id,user_id,title=None,description=None,deadline=None,category=None,priority=None,is_completed=None):
    with Session(engine,expire_on_commit=False) as session:
        task=session.query(Task).filter(Task.id==task_id).first()
        if task is None:
            return None,404
        elif task.user_id!=user_id:
            return None,401
    
        if title is not None:
            task.title=title
        if description is not None:
            task.description=description
        if deadline is not None:
            task.deadline=deadline
        if category is not None:
            task.category=category
        if is_completed is not None:
            task.is_completed=is_completed
        if priority is not None:
            task.priority=priority

        session.commit()
        session.refresh(task)
        make_transient(task)
        return task,200

def delete_task(task_id,user_id):
    with Session(engine,expire_on_commit=False) as session:
        task=session.query(Task).filter(Task.id==task_id).first()
        if task is None:
            return 404
        elif task.user_id!=user_id:
            return 401
        else:
            session.delete(task)
            session.commit()
            return 200