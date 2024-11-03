from secret import DATABASE_URL
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)