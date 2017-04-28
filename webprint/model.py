from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData, Column, Integer, DateTime, String
from sqlalchemy.orm import sessionmaker

meta = MetaData()
Base = declarative_base(metadata=meta)
Session = sessionmaker()


class Task(Base):
    __tablename__ = 'task'

    taskId = Column('task_id', Integer, primary_key=True)
    printerName = Column('printer_name', String, nullable=False)
    title = Column('title', String)
    submitTime = Column('submit_time', DateTime)
