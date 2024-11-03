import pytest
from sqlalchemy import text

from services.db_service import add_task, get_tasks_by_user_id
from data.task import Task
from data.task import Base
from data import engine
from sqlalchemy.orm import Session

example_tasks=[]

@pytest.fixture(scope="session",autouse=True)
def setup():
    global example_tasks

    example_tasks=[Task(user_id="test_1",title="test title 1"),Task(user_id="test_2",title="test title 2")]

    Base.metadata.create_all(engine)
    with Session(engine,expire_on_commit=False) as session:
        session.add(example_tasks[0])
        session.commit()

    yield

    with Session(engine,expire_on_commit=False) as session:
        tasks=session.query(Task).filter(Task.user_id=="test_1").all()
        tasks+=session.query(Task).filter(Task.user_id=="test_2").all()
        for task in tasks:
            session.delete(task)
        session.commit()


def test_add_task():
    global example_tasks

    

    with Session(engine,expire_on_commit=False) as session:
        assert(session.query(Task).filter(Task.user_id=="test_2").count()==0)

    task=example_tasks[1]
    result=add_task(user_id=task.user_id,title=task.title)

    assert(result.user_id is not None)
    assert(result.title==task.title)

    with Session(engine,expire_on_commit=False) as session:
        assert(session.query(Task).filter(Task.user_id=="test_2").count()==1)

def test_get_all_task():
    global example_tasks

    results=get_tasks_by_user_id("test_1")

    assert(len(results)==1)

    assert(results[0].user_id==example_tasks[0].user_id)

