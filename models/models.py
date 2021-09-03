from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

db = create_engine('sqlite:///D:\\Project\\TaskTracker\\db\\tasktracker.db', echo=True)

metadata_obj = MetaData()

user = Table('users', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('login', String, nullable=False, unique=True),
    Column('password', String, nullable=False),
    Column('fullname', String, nullable=False),
 )

task = Table('tasks', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', None, ForeignKey('users.id')),
    Column('description', String, nullable=False),
    Column('current_status', String, nullable=False, default='Новая'),
    Column('date_creation', String, nullable=False, default=datetime.now),
    Column('date_get_to_work', String),
    Column('date_complete', String),
    Column('date_cancel', String)
  )

lifecycle_tasks = Table('lifecycle_tasks', metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('task', None, ForeignKey('tasks.id')),
    Column('user', None, ForeignKey('users.id')),
    Column('status', String, nullable=False, default='Новая'),
    Column('date', String, nullable=False, default=datetime.now),
  )


if __name__ == '__main__':
    metadata_obj.create_all(db)