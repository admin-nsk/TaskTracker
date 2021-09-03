from models.db_worker import UserHandler, TaskHandler
from models import models
from sqlalchemy import create_engine

db = create_engine('sqlite:///:memory:', echo=True)

models.db = db

def fake_execute_query(query):
    return db.execute(query)

class TestUserHandler:

    def setup(self):
        self.user_handler = UserHandler()
        self.user_values = {
            'login': 'deletetest',
            'password': 'deletetest',
            'fullname': 'test fullname'
        }
        models.metadata_obj.create_all(db)
        self.user_handler.execute_query = fake_execute_query

    def test_create_user(self):
        self.user_handler.create(self.user_values)
        result = self.user_handler.get(self.user_values['login'])
        assert self.user_values['login'] == result.login

    def test_delete_user(self):
        user = self.user_handler.get(self.user_values['login'])
        self.user_handler.delete(user.id)
        user = self.user_handler.get(self.user_values['login'])
        assert user == None


class TestTaskHandler:

    def setup(self):
        self.task_handler = TaskHandler()
        self.task_values = {
            'description': 'test task',
        }
        self.lifecycle_values = {
            'task': 1,
            'status': 'Новая',
        }
        models.metadata_obj.create_all(db)
        self.task_handler.execute_query = fake_execute_query

    def test_create_task(self):
        result = self.task_handler.create(self.task_values, self.lifecycle_values)
        assert result is not None

    def test_get_task(self):
        result = self.task_handler.get(1)
        assert self.task_values['description'] == result.description

    def test_change_status(self):
        self.task_values['current_status'] = 'Выполнено'
        self.task_values['user_id'] = 1
        self.lifecycle_values['status'] = 'Выполнено'
        self.lifecycle_values['user'] = '1'
        self.task_handler.update(1, self.task_values, self.lifecycle_values)
        result = self.task_handler.get(1)
        assert result['current_status'] == 'Выполнено'

    def test_get_lifecycle(self):
        result = self.task_handler.get_lifecycle(1)
        assert len(result) == 2