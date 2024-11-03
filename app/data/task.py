from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Enum, ForeignKey, func
from sqlalchemy.orm import relationship,declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id=Column(String,nullable=False)
    title=Column(String,nullable=False)
    description=Column(String)
    priority=Column(Integer,default=0)
    deadline=Column(DateTime)
    is_completed=Column(Boolean,default=False)
    category=Column(String,default="default")
    created_date = Column(DateTime, server_default=func.now())

    def as_dict(self):
        result = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        for key in ['deadline']:
            if key in result and result[key] is not None:
                result[key] = result[key].isoformat()
        return result

