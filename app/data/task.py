from sqlalchemy import Column, DateTime, Integer, String, Text, Enum, ForeignKey, func
from sqlalchemy.orm import relationship,declarative_base
from . import Base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    userId=Column(String,nullable=False)
    title=Column(String,nullable=False)
    description=Column(String)
    priority=Column(Integer,server_default=0)
    deadline=Column(DateTime)
    is_completed=Column(bool,server_default=False)
    category=Column(String,server_default="default")
    created_date = Column(DateTime, server_default=func.now())

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in ['deadline']:
            if key in result and result[key] is not None:
                result[key] = result[key].isoformat()
        return result

