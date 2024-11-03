from secret import DATABASE_URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .task import Base,Task

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)