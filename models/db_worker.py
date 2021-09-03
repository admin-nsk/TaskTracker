from flask_login import UserMixin

from models.models import user, task, lifecycle_tasks, db
from sqlalchemy import select, and_
from werkzeug.security import generate_password_hash, check_password_hash


class UserHandler(UserMixin):
    def __init__(self):
        self.user_id = None
        self.user_login = None
        self.user_password = None

    def create(self, values: dict):
        values['password'] = generate_password_hash(f"{values['password']}{values['login']}")
        query = user.insert().values(**values)
        return self.execute_query(query)

    def update(self, id: int, values: dict):
        query = user.update().where(user.c.id == id).values(**values)
        return self.execute_query(query)

    def get_by_id(self, id):
        query = user.select().where(user.c.id == id)
        result = self.execute_query(query).fetchone()
        if result:
            self.user_login = result.login
            self.user_password = result.password
            self.user_id = result.id
        return result

    def get(self, login):
        query = user.select().where(user.c.login == login)
        result = self.execute_query(query).fetchone()
        if result:
            self.user_login = result.login
            self.user_password = result.password
            self.user_id = result.id
        return result

    def delete(self, id):
        query = user.delete().where(user.c.id == id)
        return self.execute_query(query)

    def check_password(self, password, login):
        query = select(user).where(user.c.login == login)
        check_user = self.execute_query(query).fetchone()
        return check_password_hash(check_user.password, f"{password}{login}")

    def execute_query(self, query):
        return db.execute(query)

    @property
    def login(self):
        return self.user_login

    @property
    def password(self):
        return self.user_password

    @property
    def id(self):
        return self.user_id


class TaskHandler:

    def create(self, values_task: dict, values_lifecycle: dict):
        query_tasks = task.insert().values(**values_task)
        result_create_task = self.execute_query(query_tasks)
        values_lifecycle['task'] = result_create_task.inserted_primary_key[0]
        self._create_lifecycle(values_lifecycle)
        return result_create_task.inserted_primary_key[0]

    def update(self, id: int, values_task: dict, values_lifecycle: dict):
        query_tasks = task.update().where(task.c.id == id).values(**values_task)
        result_create_task = self.execute_query(query_tasks)
        self._create_lifecycle(values_lifecycle)
        return result_create_task

    def get(self, id):
        query_task = task.select().where(task.c.id == id)
        return self.execute_query(query_task).fetchone()

    def _create_lifecycle(self, values_lifecycle):
        query_lifecycle = lifecycle_tasks.insert().values(**values_lifecycle)
        self.execute_query(query_lifecycle)

    def get_all(self, task_status=None):
        if task_status:

            query_task = task.select().where(task.c.current_status == task_status)
        else:
            query_task = task.select()
        return self.execute_query(query_task).fetchall()

    def get_user_task(self, user_id, task_status=None):
        if task_status:
            query_task = task.select().where(and_(task.c.user_id == user_id, task.c.current_status == task_status))
        else:
            query_task = task.select().where(task.c.user_id == user_id)
        return self.execute_query(query_task).fetchall()

    def get_lifecycle(self, task_id):
        query_lifecycle = lifecycle_tasks.select().where(lifecycle_tasks.c.task == task_id)
        return self.execute_query(query_lifecycle).fetchall()

    def delete(self):
        query = task.delete().where(task.c.id == id)
        return self.execute_query(query)

    def execute_query(self, query):
        return db.execute(query)
